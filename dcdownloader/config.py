import yaml

# 填充默认设置
default_config = {
    'debug_mode': False,
    'save_manifest_file': True,
    'output_path': './output',
    'proxy': None,
    'downloader_max_connection_number': 5,
    'downloader_max_retry_number': 5,
    'friendly_console_output': False,
    'header': {
        'referer': 'https://manhua.dmzj.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    },
}
    
config = {}

def load(text):
    global config
    config = yaml.load(text)

def load_file(file_path):
    with open(file_path) as f:
        load(f.read())

def get(key, fallback=False):
    keys = key.split('.')

    if fallback == True:
        target = default_config
    else:
        target = config
    
    for k in keys:
        target = target.get(k)
    
    if target == None and not fallback == True:
        target = get(key, fallback=True)
    return target
