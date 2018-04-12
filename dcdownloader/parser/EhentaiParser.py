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

        img_list = []
        
        for img in _img_list:
            url = pq(img).attr('href')
            img_list.append(url)
        
        next_page = doc('.ptds + td a')
        next_page_url = None
        if not next_page == None:
            next_page_url = pq(next_page).attr('href')

        return (img_list, next_page_url)
    
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