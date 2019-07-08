from pathlib import Path
import json
from flask import Flask, render_template, send_from_directory
import redis

app = Flask(__name__)
sync_file = Path('sync_file')
sync_file.touch()
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


def read_urls():
    urls = redis_conn.get('images_urls')
    urls = json.loads(urls if urls is not None else [])
    return urls


def load_image():
    pass


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
