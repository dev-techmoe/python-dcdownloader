import asyncio
import logging

import aiofiles
import aiohttp
import filetype

from dcdownloader import base_logger, utils
# for test
from dcdownloader.parser.SimpleParser import SimpleParser
from dcdownloader.utils import retry
from .aiohttp_proxy_connector import ProxyConnector
logger = base_logger.getLogger(__name__)
                                                                                                   
class Scheduler(object):
    download_total_number = 0
    download_complete_number = 0

    def __init__(self, url, output_path='.', name='Scheduler', max_connection_num=10, max_retry_num=5, 
                    proxy=None, header=None, save_manifest_file=False, parser=SimpleParser(),
                    fetch_only=False, verify_ssl=True):
        
        # usable config:
        # name: Scheduler instance name
        # url: url of target comic
        # downloader_max_connection_num: max connection number for downloading
        # downloader_max_retry_num: max retry number for downloading
        # proxy: proxy setting (e.g: http://127.0.0.1:1081)
        # header: http request header
        # save_manifest_file: (not complete)
        self.url = url
        self.output_path = output_path
        self.name = name
        self.max_connection_num = max_connection_num
        self.max_retry_num = max_retry_num
        self.proxy = proxy
        self.header = None
        self.save_manifest_file = False
        self.fetch_only = fetch_only
        self.verify_ssl = verify_ssl

        self.sema = asyncio.Semaphore(self.max_connection_num)

        self.parser = parser

        if 'request_header' in dir(self.parser):
            self.header = self.parser.request_header

        self.aiohttp_session = aiohttp.ClientSession(
            connector=ProxyConnector(proxy=proxy, verify_ssl=self.verify_ssl), headers=self.header, read_timeout=30)

    def run(self):
        logger.info('Using parser %s ..', type(self.parser).__name__)
        logger.info('Fetch information')
        info = self._get_info(self.url)

        if not info:
            logger.error('No comic infomation found.')
            return
        else:
            logger.info('Comic name: %s', info.get('name'))
        
        logger.info('Fetch chapter list')
        clist = self._get_chapter_list(base_url=self.url)

        if not clist:
            logger.error('No chapter list found')
            return
        else:
            logger.info('Chapter number: %d', len(clist))
        
        logger.info('Fetch image url list')
        img_list = self._get_image_url_list(clist)
        logger.info('Total image number: %s', self.total_image_num)
        logger.info('Start download images')
        self._start_download(img_list, info['name'])
        logger.info('Download comlpleted')

        self._close_request_session()
    
    def _get_info(self, base_url):
        info = {}

        logger.debug('Fetching target information')
        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to get info %s (%s), retrying.', args[0][0],str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to get info %s (%s)', args[0][0],str(err)),
            on_fail_exit=True) 
        async def fetch(url):
            #async with aiohttp.ClientSession(connector=ProxyConnector(proxy='http://192.168.28.1:8888')) as sess:
            async with self.aiohttp_session.get(url, verify_ssl=self.verify_ssl) as resp:
                nonlocal info
                ret_data = await resp.text()
                info = await self.parser.parse_info(ret_data)
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(fetch(base_url)))

        return info


    def _get_chapter_list(self, base_url):
        logger.debug('Starting fetch chapter list')
        chapter_list = {}

        # chapter_list = {
        #     'chapter_name': 'url'
        # }

        # @retry(stop=stop_after_attempt(self.max_retry_num))
        # @retry(max_num=self.max_retry_num)
        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to fetch chapter list %s (%s), retrying.', args[0][0],str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to fetch chapter list %s (%s)', args[0][0],str(err)),
            on_fail_exit=True) 
        async def fetch(url, asyncio_loop, page=1):
            with (await self.sema):
                async with self.aiohttp_session.get(url) as ret:

                    ret_data = await ret.text()
                    parsed_data = await self.parser.parse_chapter(ret_data)
                    
                    if self.parser.chapter_mode:
                        chapter_list.update( parsed_data[0] )
                    else:
                        for i in parsed_data[0]:
                            chapter_list.setdefault('{}-{}'.format(page,parsed_data[0].index(i)), i)
                    
                    if len(parsed_data) > 1 and not parsed_data[1] == None:
                        page += 1
                        await fetch(parsed_data[1], asyncio_loop, page)
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(fetch(base_url, loop)))

        return chapter_list
        
    
    def _get_image_url_list(self, chapter_list):

        image_url_list = {}
        
        # image_url_list = {
        #     'chapter_name': {
        #         'file_name': 'url'
        #     }
        #     # ...
        # }

        #@retry(max_num=self.max_retry_num, 
        #    on_retry=lambda err, args, num: logger.warning('Failed to fetch chapter list (%s=>%s)', args[0][0], args[0][1]))
        total_image_num = 0
        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to fetch image list "%s" (%s), retrying.', str(args[0]), str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to fetch image list "%s" (%s)', str(args[0]), str(err)),
            on_fail_exit=True)
        async def fetch(chapter_name, chapter_url):
            nonlocal total_image_num
            with (await self.sema):
                async with self.aiohttp_session.get(chapter_url, verify_ssl=self.verify_ssl) as resp:
                    image_list = await self.parser.parse_image_list(await resp.text())
                    total_image_num += len(image_list)
                    image_url_list.update({chapter_name: image_list})
        
        loop = asyncio.get_event_loop()
        future_list = []


        for k, v in chapter_list.items():
            future_list.append(fetch(k, v))
            

                
        loop.run_until_complete(asyncio.gather(*future_list))
        self.total_image_num = total_image_num
        return image_url_list
    
    def _start_download(self, image_url_list, comic_name):
        # 解藕希望

        # @retry(stop=stop_after_attempt(self.max_retry_num), after=after_log(logger, logging.DEBUG))
        #@retry(max_num=self.max_retry_num, on_retry=self._downloader_on_retry)
        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to update downloading status (%s), retrying.', str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to update downloading status (%s)', str(err)) )
        async def update_count(save_path, name):
            logger.info('Download complete: %s', self._generate_download_info(name, save_path))
            self.download_complete_number += 1
            if '_on_download_complete' in dir(self.parser):
                getattr(self, '_on_download_complete')()
        
        # @retry(stop=stop_after_attempt(self.max_retry_num), after=after_log(logger, logging.DEBUG))
        # @retry(max_num=self.max_retry_num, on_retry=self._downloader_on_retry)
        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to save file "%s" (%s), retrying.', args[1]['save_path'],str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to save file "%s" (%s)', args[1]['save_path'],str(err))) 
        async def save_file(binary, save_path, name): 
            logger.debug('Saving file %s', self._generate_download_info(name, save_path))
            async with aiofiles.open(save_path, 'wb') as f:
                await f.write(binary)
                await update_count(save_path=save_path, name=name)
        

        @retry(max_num=self.max_retry_num, 
            on_retry=lambda err, args, retry_num: logger.warning('Failed to request url "%s" (%s), retrying.', args[1]['image_url'], str(err)), 
            on_fail=lambda err, args, retry_num: logger.error('Failed to request target "%s" (%s)', args[1]['image_url'], str(err)) )
        async def download(image_url, save_path, name):
            with (await self.sema):
                logger.info('Start download: %s', self._generate_download_info(name, save_path))
                utils.mkdir('/'.join(save_path.split('/')[:-1]))
                #async with aiohttp.ClientSession(headers=self.header) as session:

                if self.fetch_only:
                    logger.warning('Fetch only mode is on, all downloading process will not run')
                    return
                
                async with self.aiohttp_session.get(image_url, verify_ssl=self.verify_ssl) as resp:
                    resp_data = await resp.content.read()
                    if 'on_download_complete' in dir(self.parser):
                        resp_data = getattr(self.parser, 'on_download_complete')(resp_data)

                    if 'filename_extension' in dir(self.parser):
                        filename_extension = self.parser.filename_extension
                    else:
                        filename_extension = filetype.guess(resp_data).extension
                    
                    if filename_extension:
                        save_path += '.' + filename_extension
                    else:
                        logger.warning('unknown filetype')
                    
                    # return (resp_data, save_file)
                    await save_file(binary=resp_data, save_path=save_path, name=name)
            
        loop = asyncio.get_event_loop()
        future_list = []

        
        for k, v in image_url_list.items():
            for name, url in v.items():
                # future_list.append(download(url, path + ))
                # path = '_temp/' + comic_name +  k + '/'+ name
                if 'chapter_mode' in dir(self.parser) and not self.parser.chapter_mode:
                    path = '/'.join([self.output_path, comic_name, name])
                else:
                    path = '/'.join([self.output_path, comic_name, k, name])

                future_list.append(download(image_url=url, save_path=path, name=name))
        
        loop.run_until_complete(asyncio.gather(*future_list))
    

    def _generate_download_info(self, name, path):
        return name + ' => '+ path


    def _downloader_on_retry(self, err, args, retry_num):
        logger.warning('Download fail (%s) %s, retry number: %s', str(err), 
            self._generate_download_info(args[1]['name'], args[1]['save_path']), retry_num)

    def _close_request_session(self):
        asyncio.get_event_loop().run_until_complete(asyncio.gather(self.aiohttp_session.close()))

    def __del__(self):
        self._close_request_session()
    def _on_download_complete(self):
        pass
    
    def _call_parser_hook(self, hook_name):
        pass
