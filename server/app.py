from pathlib import Path
import json
from io import BytesIO
import base64
from flask import Flask, render_template, send_file
import redis

app = Flask(__name__)
sync_file = Path('sync_file')
sync_file.touch()
redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)


def read_urls():
    urls = redis_conn.get('images_urls')
    urls = json.loads(urls if urls is not None else '[]')
    return urls


def load_image(filename):
    img = redis_conn.get(filename)
    return img


@app.route('/')
def index():
    sync_file.touch()
    urls = read_urls()
    t_shirt_images, images = read_imgs()
    urls = zip(urls, t_shirt_images, images)
    return render_template('index.html',
                           urls=urls)


# @app.route('/images/<filename>.png')
# def serve_image(filename):
#     img = load_image(filename)
#     return send_file(BytesIO(img),
#                      mimetype='image/png',
#                      cache_timeout=-1)

def get_image(filename):
    img = load_image(filename)
    # img = BytesIO(img).get_value().
    # img = img.encode('base64')
    img = base64.b64encode(img)
    return img


def read_imgs():
    t_shirt_image_names = [f't_shirt_image_{i}' for i in range(9)]
    image_names = [f'image_{i}' for i in range(9)]

    t_shirt_images = [get_image(name) for name in t_shirt_image_names]
    images = [get_image(name) for name in image_names]
    return t_shirt_images, images


if __name__ == '__main__':
    app.run(host='0.0.0.0')
