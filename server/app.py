import random
import time
import os
from flask import Flask, render_template, send_from_directory
import boto3
from PIL import Image
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import threading


app = Flask(__name__)

images_path = 'images'
t_shirt_path = 't_shirt'
current_image = 0
batch_size = 9
max_images = 21981
update_delta = 15  # 60
last_update = 0
# random.seed(24)

client = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWSAccessKeyId'],
    aws_secret_access_key=os.environ['AWSSecretKey'],
    region_name='eu-central-1'
)

server_images_index = list(range(max_images))
random.shuffle(server_images_index)

logo = Image.open('static/logo_op.png', 'r')
logo.load()
background = Image.open('static/t_shirt.jpg', 'r')

# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True


def make_t_shirt_and_small(i):
    img = Image.open('{}/image_{}.png'.format(images_path, i), 'r')

    # insert logo
    img_w, img_h = img.size
    offset = (img_w // 80 * 71, img_h // 30 * 29)
    img.paste(logo, offset, mask=logo.split()[3])
    img.save('{}/image_{}.png'.format(images_path, i))

    # make small image
    bg_w, bg_h = background.size
    img = img.resize((bg_w, bg_h))
    img.save('{}/image_{}_small.png'.format(images_path, i))

    # insert image in t-shirt
    img = img.resize((bg_w // 10 * 4, bg_h // 10 * 4))
    img_w, img_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 10 * 6)
    background.paste(img, offset)

    background.save('{}/image_{}.png'.format(t_shirt_path, i))

    img.close()


def download_and_process_image(i, server_index):
    client.download_file('ganarts',
                         '{}/image_{}.png'.format(images_path,
                                                  server_index),
                         '{}/image_{}.png'.format(images_path, i))
    make_t_shirt_and_small(i)


def download_next_images():
    """
    Shuffle s3 images index and iterating in it.
    Download batch_size images from s3 and save in with names from 0 to 9.png.
    When s3 images end, shuffle and start iterating from the beginning.
    Inserting my logo, creating small version of image, insert image in t-shirt.
    """
    global current_image
    server_indexes = []

    for i in range(batch_size):
        server_indexes.append(server_images_index[current_image])

        current_image += 1
        if current_image >= max_images:
            current_image = 0
            random.shuffle(server_images_index)

    for i, server_index in enumerate(server_indexes):
        download_and_process_image(i, server_index)

        # t = threading.Thread(target=download_and_process_image, args=tup)
        # t.start()
        # t.join()


def update_images():
    global last_update
    cur_time = time.time()
    if cur_time - last_update > update_delta:
        download_next_images()
        last_update = cur_time


@app.route('/')
def index():
    update_images()
    return render_template('index.html')


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(images_path,
                               filename,
                               as_attachment=True,
                               cache_timeout=-1)


@app.route('/t_shirt/<filename>')
def serve_t_shirt(filename):
    return send_from_directory(t_shirt_path,
                               filename,
                               cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


def benchmark():
    for i in range(3):
        start = time.time()
        download_next_images()
        print('{:.2f}'.format(time.time() - start))