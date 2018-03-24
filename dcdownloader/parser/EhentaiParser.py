from pyquery import PyQuery as pq

from abc import ABCMeta, abstractmethod

class EhentaiParser(metaclass=ABCMeta):
    base_url = ''
    chapter_mode = False

    async def parse_info(self, data):
        doc = pq(data)
        name = doc('#gn').text()
        
        return {'name': name}
    
    async def parse_chapter(self, data):
        doc = pq(data)
        _img_list = doc('.gdtm a')

        i = 1
        img_list = {}
        
        for img in _img_list:
            url = pq(img).attr('href')
            img_list.setdefault(str(i), url)
            i += 1
        
        return (img_list, )
    
    async def parse_image_list(self, data):
        doc = pq(data)
        img_name = pq(doc('#i2 div')[2]).text().split('.')[0]
        img_url =  doc('#i3 img').attr('src')

        return {
            img_name: img_url
        }
        # return {
        #     'file_name': 'url'
        # }
        pass

    async def parse_downloaded_data(self, data):
        pass