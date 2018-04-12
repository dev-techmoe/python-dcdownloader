from abc import ABCMeta, abstractmethod

class BaseParser(metaclass=ABCMeta):

    # filename extension for downloaded file
    filename_extension = None
    # request_header
    request_header = None

    # if target website not has the chapter list
    # e.g. Ehentai
    # turn this attribute to False
    chapter_mode = True

    @abstractmethod
    async def parse_info(self, data):
        """ Get detail of target page (e.g.: name, author, etc.)
            Args:
                data: data come from requesting specified URL.
            
            Returns:
                {
                    'name': '...'
                }
        """
    

    @abstractmethod
    async def parse_chapter(self, data, page):
        """ Parse chapter data from received data.
            Args:
                data: data come from requesting specified URL.

            Returns: 
                if self.chapter_mode == True (default):
                (
                    {
                        'chapter_name': 'url'
                    },
                    'url_of_next_chapter_page(optional)'
                )
                else:
                (
                    (<url1>, <url2>, <url3>, ...),
                    'url_of_next_chapter_page(optional)'
                )
                Return must be a list
        """
    
    @abstractmethod
    async def parse_image_list(self, data):
        """ Parse image URL from received data.
            Args:
                data: data come from requesting specified URL.
            
            Returns:
                {
                    'file_name': 'url'
                }
        """
    
    async def parse_downloaded_data(self, data):
        """ Process the downloaded data. (optional)
            You can do some action (such as decrypt, unzip, etc) in there
            Args:
                data: data come from requesting specified URL.
            
            Returns:
                processed data
        """