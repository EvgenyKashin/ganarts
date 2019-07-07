from pathlib import Path
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
sync_file = Path('sync_file')
sync_file.touch()


def read_urls():
    with open('images/urls.txt') as f:
        urls = f.readlines()
    return urls


@app.route('/')
def index():
    sync_file.touch()
    urls = read_urls()
    return render_template('index.html',
                           urls=urls)


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory('images',
                               filename,
                               cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
