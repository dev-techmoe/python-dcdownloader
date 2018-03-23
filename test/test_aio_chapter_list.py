from test.bootstrap import dcdownloader
import dcdownloader.aio_chapter_list as aio_chapter_list

def test_parse_comic_chapter_list():
    true_result = ('kanon & AIR', {'14话': 'https://manhua.dmzj.com/kanonair/734.shtml', '06话': 'https://manhua.dmzj.com/kanonair/726.shtml', '04话': 'https://manhua.dmzj.com/kanonair/724.shtml', '07话': 'https://manhua.dmzj.com/kanonair/727.shtml', '03话': 'https://manhua.dmzj.com/kanonair/723.shtml', '05话': 'https://manhua.dmzj.com/kanonair/725.shtml', '11话': 'https://manhua.dmzj.com/kanonair/731.shtml', '09话': 'https://manhua.dmzj.com/kanonair/729.shtml', '10话': 'https://manhua.dmzj.com/kanonair/730.shtml', '01话': 'https://manhua.dmzj.com/kanonair/721.shtml', '12话': 'https://manhua.dmzj.com/kanonair/732.shtml', '02话': 'https://manhua.dmzj.com/kanonair/722.shtml', '13话': 'https://manhua.dmzj.com/kanonair/733.shtml', '08话': 'https://manhua.dmzj.com/kanonair/728.shtml'})

    ret = aio_chapter_list.parse_comic_chapter_list('https://manhua.dmzj.com/kanonair/')

    assert ret == true_result

def test_fetch_all_image_list():
    true_result = {'01话': ['https://images.dmzj.com/k/konanair/01/001.jpg', 'https://images.dmzj.com/k/konanair/01/002.jpg', 'https://images.dmzj.com/k/konanair/01/003.jpg', 'https://images.dmzj.com/k/konanair/01/004.jpg', 'https://images.dmzj.com/k/konanair/01/005.jpg', 'https://images.dmzj.com/k/konanair/01/006.jpg', 'https://images.dmzj.com/k/konanair/01/007.jpg', 'https://images.dmzj.com/k/konanair/01/008.jpg', 'https://images.dmzj.com/k/konanair/01/009.jpg', 'https://images.dmzj.com/k/konanair/01/010.jpg', 'https://images.dmzj.com/k/konanair/01/011.jpg', 'https://images.dmzj.com/k/konanair/01/012.jpg', 'https://images.dmzj.com/k/konanair/01/013.jpg', 'https://images.dmzj.com/k/konanair/01/014.jpg', 'https://images.dmzj.com/k/konanair/01/015.jpg', 'https://images.dmzj.com/k/konanair/01/016.jpg', 'https://images.dmzj.com/k/konanair/01/017.jpg', 'https://images.dmzj.com/k/konanair/01/018.jpg', 'https://images.dmzj.com/k/konanair/01/019.jpg', 'https://images.dmzj.com/k/konanair/01/020.jpg', 'https://images.dmzj.com/k/konanair/01/021.jpg', 'https://images.dmzj.com/k/konanair/01/022.jpg', 'https://images.dmzj.com/k/konanair/01/023.jpg', 'https://images.dmzj.com/k/konanair/01/024.jpg', 'https://images.dmzj.com/k/konanair/01/025.jpg', 'https://images.dmzj.com/k/konanair/01/026.jpg']}

    ret = aio_chapter_list.fetch_all_image_list({'01话': 'https://manhua.dmzj.com/kanonair/721.shtml'})

    assert ret == true_result