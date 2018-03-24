from dcdownloader.parser.BaseParser import BaseParser
from pyquery import PyQuery as pq

class SimpleParser(BaseParser):
    
    async def parse_info(self, data):
        doc = pq(data)
        name = doc('h1').text()

        output = {}
        if name:
            output.setdefault('name', name)

        return output
    
    async def parse_chapter(self, response_data):
        doc = pq(response_data)
        data = {}
        for i in doc('.chapter_list a'):
            data.setdefault(i.text, pq(i).attr('href'))
        return (data,)
    
    async def parse_image_list(self, response_data):
        doc = pq(response_data)
        data = {}

        for i in doc('ul li img'):
            data.setdefault(pq(i).attr('alt'), pq(i).attr('src'))
        
        return data

                               
    async def parse_downloaded_data(self, data):
        pass