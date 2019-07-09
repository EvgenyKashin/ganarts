from pathlib import Path
import json
from io import BytesIO
from flask import Flask, render_template, send_file
import redis

app = Flask(__name__)
sync_file = Path('sync_file')
sync_file.touch()
redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)


def read_urls():
    urls = redis_conn.get('images_urls')
    urls = json.loads(urls if urls is not None else [])
    return urls


def load_image(filename):
    img = redis_conn.get(filename)
    return img


@app.route('/')
def index():
    sync_file.touch()
    urls = read_urls()
    return render_template('index.html',
                           urls=urls)


@app.route('/images/<filename>.png')
def serve_image(filename):
    img = load_image(filename)
    return send_file(BytesIO(img),
                     mimetype='image/png',
                     cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
