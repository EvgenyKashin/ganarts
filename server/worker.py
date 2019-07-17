import os
import time
from pathlib import Path
import random
from io import BytesIO
import json
import boto3
from PIL import Image
import redis


images_path = 'small_images'
t_shirt_path = 't_shirt'
batch_size = 9
current_image = 0
max_images = 21979
update_delta = 30
bucket = 'ganarts'
expires_hours = 24

client_s3 = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWSAccessKeyId'],
    aws_secret_access_key=os.environ['AWSSecretKey'],
    region_name='eu-central-1'
)

redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)

server_images_index = list(range(max_images))
random.shuffle(server_images_index)
background = Image.open('static/t_shirt.jpg', 'r')

sync_file = Path('sync_file')
sync_file.touch()
prefix_file = Path('prefix_file')
prefix_file.touch()

def make_t_shirt(img):
    bg_w, bg_h = background.size

    # insert image in t-shirt
    img = img.resize((bg_w // 10 * 4, bg_h // 10 * 4))
    img_w, img_h = img.size

    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 10 * 6)
    background.paste(img, offset)

    return background


def download_and_process_image(server_index):
    response = client_s3.get_object(Bucket=bucket,
                                    Key='{}/image_{}.png'.format(images_path,
                                                                 server_index))
    content = response['Body']
    img = Image.open(content)
    img_t_shirt = make_t_shirt(img)

    output_img = BytesIO()
    output_img_t_shirt = BytesIO()
    img.save(output_img, format=img.format)
    img_t_shirt.save(output_img_t_shirt, format=img_t_shirt.format)

    return output_img, output_img_t_shirt


def make_urls(indexes):
    urls = []
    for i in indexes:
        url = client_s3.generate_presigned_url(
                                            'get_object',
                                            Params={
                                                'Bucket': bucket,
                                                'Key': f'images_with_logo/'
                                                       f'image_{i}.png'},
                                            ExpiresIn=60 * 60 * expires_hours)
        urls.append(url)
    return urls


def save_to_redis(images_files, images_urls, prefix):
    """
    Not such beautiful, like inplace image saving, but it execute
    all commands in one transaction. It wasn't possible with saving
    files to filesystem(without redis).
    """
    pipeline = redis_conn.pipeline()

    # save images
    for i, (image, t_shirt_image) in enumerate(images_files):
        pipeline.set(f'{prefix}_image_{i}', image.getvalue())
        pipeline.set(f'{prefix}_t_shirt_image_{i}', t_shirt_image.getvalue())
        image.close()
        t_shirt_image.close()

    # save full size images(s3 urls)
    pipeline.set(f'{prefix}_images_urls', json.dumps(images_urls))
    pipeline.execute()


def download_next_images(prefix):
    """
    Shuffle s3 images index and iterating in it.
    Download batch_size images from s3 and save in with names from 0 to 9.png.
    When s3 images end, shuffle and start iterating from the beginning.
    Insert image in t-shirt.
    """
    global current_image
    server_indexes = []

    for i in range(batch_size):
        server_indexes.append(server_images_index[current_image])

        current_image += 1
        if current_image >= max_images:
            current_image = 0
            random.shuffle(server_images_index)

    downloaded_images_files = []
    for server_index in server_indexes:
        downloaded_images_files.append(download_and_process_image(server_index))

    images_urls = make_urls(server_indexes)
    s = time.time()
    save_to_redis(downloaded_images_files, images_urls, prefix)
    # TODO: logging
    print(f'Transaction time: {time.time() - s:.3f}s', flush=True)


def update_images():
    last_update = 0
    st_atime = 0
    prefix_alternates = ['a', 'b']
    step = 0

    while True:
        cur_time = time.time()
        if cur_time - last_update > update_delta and\
           cur_time - st_atime < update_delta * 2:
            last_update = time.time()
            prefix = prefix_alternates[step % 2]

            download_next_images(prefix)
            prefix_file.write_text(prefix)
            step += 1
            # TODO: logging
            print(f'Step {step}, downloading: {time.time() - last_update:.3f}s',
                  flush=True)
        else:
            time.sleep(0.1)
            st_atime = sync_file.stat().st_atime


if __name__ == '__main__':
    update_images()


