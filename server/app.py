from pathlib import Path
import random
import time
from flask import Flask, render_template, send_from_directory
import boto3

app = Flask(__name__, template_folder='static')
images_path = Path('server/images')
all_images = list(images_path.iterdir())

update_delta = 10
last_update = time.time()


def update_images():
    global last_update
    cur_time = time.time()
    if cur_time - last_update > update_delta:
        random.shuffle(all_images)
        last_update = cur_time


@app.route('/')
def index():
    update_images()
    return render_template('index.html')


@app.route('/images/<filename>')
def serve_image(filename):
    position = int(filename.split('.')[0].split('_')[1])
    return send_from_directory(images_path.name,
                               all_images[position].name,
                               cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')