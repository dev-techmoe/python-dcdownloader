import asyncio, aiohttp, aiofiles, os, traceback
from dcdownloader import base_logger, config, utils
from dcdownloader.utils import update_window_title

logger = base_logger.getLogger(__name__)

# 并发数
sema = asyncio.Semaphore(config.get('downloader_max_connection_number'))
max_retry_count = config.get('downloader_max_retry_number')

get_file_name = lambda x:x.split('/')[-1]

proj_dir = ''
total_task_num = 0
completed_task_num = 0

def update_count():
    global completed_task_num
    completed_task_num += 1
    update_window_title(mode='Download', msg='{0}/{1} {2}%'.format(
        completed_task_num, total_task_num, int( (completed_task_num / total_task_num) * 100 ) ))

async def download_file(url, retry_count=0):

    async with aiohttp.ClientSession(headers=config.get('header')) as session:
        try:
            async with session.get(**utils.generate_aiohttp_session_config(url=url)) as resp:
                logger.debug('{url} response code: {code}'.format(code=resp.status, url=url))

                return await resp.content.read()
        except Exception as err:
            logger.error('download failed url = %s (%s) retry count = %s' % (url, str(err), retry_count))
            if config.get('debug_mode'):
                print(traceback.print_exc())
            if retry_count == max_retry_count:
                return 
            
            retry_count = retry_count + 1
            return await download_file(url, retry_count)
        

async def save_file(binary, save_path):
    
    async with aiofiles.open(save_path, 'wb') as f:
        data = binary
        await f.write(data)
        logger.info('download complete %s', save_path)
        update_count()


async def download(url, sub_path):
    with (await sema):
        logger.info('start download %s' % get_file_name(url))
        if not os.path.exists(proj_dir + '/' + sub_path):
            os.mkdir(proj_dir + '/' + sub_path)
        
        await save_file(await download_file(url), proj_dir + '/' + sub_path + '/ ' + get_file_name(url))
        




def launch_downloader(project_name, urls=dict(), output_path=config.get('output_path')):
    global proj_dir, total_task_num
    
    proj_dir = output_path + '/' + project_name
    utils.mkdir(proj_dir)

    events = []
    

    for k in urls.keys():
        for u in urls[k]:
            logger.debug('create download {file_name}@{chapter_name} => {url}'.format(
                file_name=get_file_name(u),
                chapter_name=k,
                url=u
            ))
            events.append(download(u, k))
    total_task_num = len(events)
    
    if not os.path.exists(proj_dir):
        os.mkdir(proj_dir)
    update_window_title(mode='Download')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(events))
    
        