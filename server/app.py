import random
import time
import os
from flask import Flask, render_template, send_from_directory
import boto3

app = Flask(__name__, template_folder='static')

images_path = 'images'
current_image = 0
batch_size = 9
max_images = 1024
update_delta = 10
last_update = 0
random.seed(24)

client = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWSAccessKeyId'],
    aws_secret_access_key=os.environ['AWSSecretKey'],
    region_name='eu-central-1'
)

server_images_index = list(range(max_images))
random.shuffle(server_images_index)


def download_next_images():
    """
    Shuffle s3 images index and iterating in it.
    Download batch_size images from s3 and save in with names from 0 to 9.png.
    When s3 images end, shuffle and start iterating from the beginning.
    """
    global current_image
    for i in range(batch_size):
        server_index = server_images_index[current_image]
        client.download_file('ganarts',
                             '{}/image_{}.png'.format(images_path,
                                                      server_index),
                             '{}/image_{}.png'.format(images_path, i))

        current_image += 1
        if current_image >= max_images:
            current_image = 0
            random.shuffle(server_images_index)


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
                               cache_timeout=-1)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
