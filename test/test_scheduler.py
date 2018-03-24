from test.bootstrap import dcdownloader
from dcdownloader.scheduler import Scheduler
from test.testserver.server import book

class TestScheduler(object):
    
    test_server_url = 'http://localhost:32321'
    s = Scheduler(test_server_url, output_path='/tmp')

    def test___get_chapter_list(self):
        correct_result = {}
        for k in book.keys():
            correct_result.setdefault(k, '/' + k)

        result = self.s._get_chapter_list(self.test_server_url)
        
        assert result == correct_result

    def test__get_image_url_list(self):
        
        target_url_list = {}
        for k in book.keys():
            target_url_list.setdefault(k, self.test_server_url +'/' + k)

        result = self.s._get_image_url_list(target_url_list)

        assert result == book

    def test__start_download(self):
        test_data = book
        for (a, b) in test_data.items():
            for (c, d) in test_data[a].items():
                test_data[a][c] = self.test_server_url + test_data[a][c]
        
        self.s._start_download(test_data, 'test')

    def test__get_info(self):
        info = self.s._get_info(self.test_server_url)

        assert info['name'] == 'test_comic'