from flask import Flask, send_from_directory
app = Flask(__name__)
from flask import render_template
from threading import Thread

book = {
    'chapter_1': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    },
        'chapter_1': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    },
        'chapter_2': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    },
        'chapter_3': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    },
        'chapter_4': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    },
        'chapter_5': {
        '1': '/static/test.png',
        '2': '/static/test.png',
        '3': '/static/test.png',
        '4': '/static/test.png',
        '5': '/static/test.png'
    }
}

index_template = r"""

"""

chapter_num_per_page = 3

@app.route('/static/<path>')
def re_static(path):
    return send_from_directory('static', path)

@app.route('/')
def main():
    return render_template('index.html', chapter_list=book.keys())

@app.route('/<chapter_id>')
def chapter(chapter_id):
    if chapter_id in book:
        return render_template('chapter.html', images=book[chapter_id])
    else:
        return 'chapter not found'

class ServerThread(Thread):
    def run(self):
        app.debug = False
        app.run(port=32321, debug=False, use_reloader=False, threaded=True)

def launch():
    ServerThread().start()

if __name__ == '__main__':
    launch()