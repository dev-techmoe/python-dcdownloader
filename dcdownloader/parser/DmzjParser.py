from dcdownloader.parser.BaseParser import BaseParser
from pyquery import PyQuery as pq
from dcdownloader import utils
import json, re, urllib

class DmzjParser(BaseParser):
    image_base_url = 'https://images.dmzj.com'
    page_base_url = 'https://manhua.dmzj.com'
    filename_extension = 'jpg'
    request_header = {
        'referer': 'https://manhua.dmzj.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
    }

    async def parse_info(self, data):
        doc = pq(data)
        comic_name = doc('.anim_title_text h1').text()

        return {
            'name': comic_name
        }

    async def parse_chapter(self, data):
        doc = pq(data)
        url_list = {}
        d = doc('.cartoon_online_border ul li a')

        for u in doc('.cartoon_online_border ul li a'):
            url_list.setdefault(pq(u).text(), self.page_base_url + pq(u).attr('href'))
        
        return (url_list, )
    
    async def parse_image_list(self, data):
        jspacker_string = re.search(r'(eval\(.+\))', data).group()
        jspacker_string = utils.decode_packed_codes(jspacker_string)

        image_list = re.search(r'(\[.+\])', jspacker_string).group()
        image_list = urllib.parse.unquote(image_list).replace('\\', '')
        image_list = json.loads(image_list)

        images = {}

        for k in image_list:
            images.setdefault(k.split('/')[-1].split('.')[0], self.image_base_url + '/' + k)
        return images