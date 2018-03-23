from test.bootstrap import dcdownloader
import dcdownloader.aiodownloader as aiodownloader

def test_launch_downloader():
    output_path = '/tmp/test/temp'
    urls = {
        'testchapter': {
            'https://i.loli.net/2018/03/23/5ab4dc247723c.jpg?a=1.jpg': '01',
            'https://i.loli.net/2018/03/23/5ab4dc247723c.jpg?a=2.jpg': '02',
            'https://i.loli.net/2018/03/23/5ab4dc247723c.jpg?a=3.jpg': '03'
        }
    }
    proj_name = 'test'
    aiodownloader.launch_downloader(
        project_name=proj_name,
        urls=urls,
        output_path=output_path
    )