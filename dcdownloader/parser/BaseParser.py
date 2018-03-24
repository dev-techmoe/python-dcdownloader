from abc import ABCMeta, abstractmethod

class BaseParser(metaclass=ABCMeta):
    base_url = ''

    @abstractmethod
    async def parse_info(self, data):
        # return {
        #     'name': '...'
        # }
        pass
    
    @abstractmethod
    async def parse_chapter(self, data):
        # return (
        #     {
        #         'chapter_name': 'url'
        #     },
        #     'url_of_next_chapter_page(optional)'
        # )
        # return must be a list
        pass
    
    @abstractmethod
    async def parse_image_list(self, data):
        # return {
        #     'file_name': 'url'
        # }
        pass

    @abstractmethod
    async def parse_downloaded_data(self, data):
        pass