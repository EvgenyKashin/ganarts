import os
import time
from pathlib import Path
import shutil
import random
import boto3
from PIL import Image


images_path = 'small_images'
t_shirt_path = 't_shirt'
batch_size = 9
current_image = 0
max_images = 21979
update_delta = 15  # 60
bucket = 'ganarts'

client = boto3.client(
    's3',
    aws_access_key_id=os.environ['AWSAccessKeyId'],
    aws_secret_access_key=os.environ['AWSSecretKey'],
    region_name='eu-central-1'
)


server_images_index = list(range(max_images))
random.shuffle(server_images_index)
background = Image.open('static/t_shirt.jpg', 'r')
sync_file = Path('sync_file')


def make_t_shirt(i, save_folder):
    img = Image.open('{}/image_{}.png'.format(save_folder, i))
    bg_w, bg_h = background.size

    # insert image in t-shirt
    img = img.resize((bg_w // 10 * 4, bg_h // 10 * 4))
    img_w, img_h = img.size

    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 10 * 6)
    background.paste(img, offset)

    background.save('{}/t_shirt_image_{}.png'.format(save_folder, i))


def download_and_process_image(i, server_index, save_folder):
    client.download_file(bucket,
                         '{}/image_{}.png'.format(images_path,
                                                  server_index),
                         '{}/image_{}.png'.format(save_folder, i))
    make_t_shirt(i, save_folder)


def make_urls(indexes):
    urls = []
    for i in indexes:
        url = client.generate_presigned_url(
                                            'get_object',
                                            Params={
                                                'Bucket': bucket,
                                                'Key': f'images_with_logo/'
                                                       f'image_{i}.png'},
                                            ExpiresIn=60 * 60)
        urls.append(url)
    return urls


def download_next_images(save_folder):
    """
    Shuffle s3 images index and iterating in it.
    Download batch_size images from s3 and save in with names from 0 to 9.png.
    When s3 images end, shuffle and start iterating from the beginning.
    Insert image in t-shirt.
    """
    global current_image
    server_indexes = []

    shutil.rmtree(str(save_folder), ignore_errors=True)
    save_folder.mkdir()

    for i in range(batch_size):
        server_indexes.append(server_images_index[current_image])

        current_image += 1
        if current_image >= max_images:
            current_image = 0
            random.shuffle(server_images_index)

    for i, server_index in enumerate(server_indexes):
        download_and_process_image(i, server_index, save_folder)

    image_urls = make_urls(server_indexes)
    with open(save_folder / 'urls.txt', 'w') as f:
        f.writelines([s + '\n' for s in image_urls])


def update_images():
    last_update = 0
    st_atime = os.stat(sync_file).st_atime
    save_folder = Path('images')
    save_temp_folder = Path('temp_images')

    download_next_images(save_temp_folder)
    save_folder.mkdir(exist_ok=True)

    while True:
        cur_time = time.time()
        if cur_time - last_update > update_delta and\
           cur_time - st_atime < update_delta * 2:
            s = time.time()
            shutil.rmtree(str(save_folder))
            shutil.move(str(save_temp_folder), str(save_folder))
            print(f'rm and mv: {time.time() - s:.3f}s')
            last_update = time.time()

            download_next_images(save_temp_folder)
            print(f'Downloading: {time.time() - last_update:.3f}s')
        else:
            time.sleep(0.1)
            st_atime = os.stat(sync_file).st_atime


if __name__ == '__main__':
    update_images()


