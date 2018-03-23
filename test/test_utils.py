from test.bootstrap import dcdownloader
from dcdownloader import utils 
import os

def test_update_window_title():
    utils.update_window_title(msg='test')

def test_generate_aiohttp_session_config():
    out = utils.generate_aiohttp_session_config(key='value')
    assert out['key'] == 'value'
    assert out['proxy'] == dcdownloader.config.get('proxy')

def test_mkdir():
    test_path = '/tmp/abc/def'
    utils.mkdir(test_path)

    assert os.path.exists(test_path)