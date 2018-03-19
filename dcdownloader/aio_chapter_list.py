import aiohttp
from pyquery import PyQuery as pq
import urllib, asyncio, re, json
from dcdownloader import utils, config, base_logger
from dcdownloader.utils import update_window_title

logger = base_logger.getLogger(__name__)
sema = asyncio.Semaphore(config.get('downloader_max_connection_number'))



def parse_comic_chapter_list(url):
    logger.debug('Fetching comic chapter list page (%s)', url)
    base_url = 'https://manhua.dmzj.com'

    async def get():
        async with aiohttp.ClientSession() as session:
            async with session.get(**utils.generate_aiohttp_session_config(url=url)) as ret:
                return await ret.text()

    loop = asyncio.get_event_loop()
    html_text = loop.run_until_complete(asyncio.gather(*[get()]))
    

    doc = pq(html_text[0])

    url_list = {}
    d = doc('.cartoon_online_border ul li a')

    for u in doc('.cartoon_online_border ul li a'):
        url_list.setdefault(pq(u).text(), base_url + pq(u).attr('href'))
    
    title = doc('.anim_title_text h1').text()

    logger.debug('Chapter list page fetching complete. Page number: %s', len(url_list))
    return (title, url_list)

def fetch_all_image_list(chapter_page_list):
    base_url = 'https://images.dmzj.com/'

    all_image_list = {}
    processing_status = {
        'completed': 0,
        'total': len(chapter_page_list)
    }

    async def fetch_image_list(chapter_name, url):
        with (await sema):
            logger.debug('Starting fetch chapter page %s => %s', chapter_name, url)

            async with aiohttp.ClientSession() as session:
                async with session.get(**utils.generate_aiohttp_session_config(url=url)) as resp:

                    text = await resp.text()
                    logger.debug('Http response code %s => %s', chapter_name, resp.status)

                    jspacker_string = re.search(r'(eval\(.+\))', text).group()
                    jspacker_string = utils.decode_packed_codes(jspacker_string)

                    image_list = re.search(r'(\[.+\])', jspacker_string).group()
                    image_list = urllib.parse.unquote(image_list).replace('\\', '')
                    image_list = json.loads(image_list)

                    image_list_ = []
                    for u in image_list:
                        image_list_.append(base_url + u)

                    all_image_list.setdefault(chapter_name, image_list_)

                    processing_status['completed'] += 1
                    update_window_title(mode='Fetching', msg="{0}/{1} {2}%".format(
                        processing_status['completed'], processing_status['total'], 
                        int( ( processing_status['completed'] / processing_status['total']) * 100 )) )
                    
                    

    
    coroutine_list = []
    for k in chapter_page_list.keys():
        coroutine_list.append(fetch_image_list(k, chapter_page_list[k]))

    loop = asyncio.get_event_loop()    
    loop.run_until_complete(asyncio.wait(coroutine_list))
    logger.debug('All chapter page fetching complete.')
    return all_image_list
    


