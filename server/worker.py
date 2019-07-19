import os
import time
import random
from io import BytesIO
import json
from pathlib import Path
from PIL import Image
import boto3
import redis


IMAGES_PATH = 'small_images'
T_SHIRT_PATH = 't_shirt'
BATCH_SIZE = 9
MAX_IMAGES = 21979
UPDATE_DELTA = 30
BUCKET = 'ganarts'
EXPIRES_HOURS = 24


class Worker:
    """
    Worker class download new batch of images and urls each UPDATE_DELTA
    and store it to redis.
    """
    def __init__(self):
        self.client_s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWSAccessKeyId'],
            aws_secret_access_key=os.environ['AWSSecretKey'],
            region_name='eu-central-1'
        )
        self.redis_conn = redis.StrictRedis(host='redis', port=6379, db=0)

        self.server_images_index = list(range(MAX_IMAGES))
        random.shuffle(self.server_images_index)
        self.current_image = 0
        self.background_img = Image.open('static/t_shirt.jpg', 'r')

        self.sync_file = Path('sync_file')
        self.sync_file.touch()
        self.prefix_file = Path('prefix_file')
        self.prefix_file.touch()

    def _make_t_shirt(self, img):
        """Insert image to T-shirt background"""
        t_shirt = self.background_img
        bg_w, bg_h = t_shirt.size

        img = img.resize((bg_w // 10 * 4, bg_h // 10 * 4))
        img_w, img_h = img.size

        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 10 * 6)
        t_shirt.paste(img, offset)

        return t_shirt

    def _download_and_process_image(self, server_index):
        """Download image from s3, make T-shirt and saving to Bytes"""
        response = self.client_s3.get_object(Bucket=BUCKET,
                                             Key='{}/image_{}.png'.format(
                                                 IMAGES_PATH, server_index))
        content = response['Body']
        img = Image.open(content)
        img_t_shirt = self._make_t_shirt(img)

        output_img = BytesIO()
        output_img_t_shirt = BytesIO()
        img.save(output_img, format=img.format)
        img_t_shirt.save(output_img_t_shirt, format=img_t_shirt.format)

        return output_img, output_img_t_shirt

    def _make_urls(self, indexes):
        """Create public available s3 urls for images"""
        urls = []
        for i in indexes:
            url = self.client_s3.\
                generate_presigned_url('get_object',
                                       Params={
                                           'Bucket': BUCKET,
                                           'Key': f'images_with_logo/'
                                                  f'image_{i}.png'},
                                       ExpiresIn=60 * 60 * EXPIRES_HOURS)
            urls.append(url)
        return urls

    def _save_to_redis(self, images_files, images_urls, prefix):
        """
        Save images(bytes) and urls with current prefix to redis.
        Not such beautiful, like inplace image saving, but it execute
        all commands in one transaction. It wasn't possible with saving
        files to filesystem(without redis).
        """
        pipeline = self.redis_conn.pipeline()

        # save images to redis in one transaction
        for i, (image, t_shirt_image) in enumerate(images_files):
            pipeline.set(f'{prefix}_image_{i}', image.getvalue())
            pipeline.set(f'{prefix}_t_shirt_image_{i}', t_shirt_image.getvalue())
            image.close()
            t_shirt_image.close()

        # save full size images(s3 urls)
        pipeline.set(f'{prefix}_images_urls', json.dumps(images_urls))
        pipeline.execute()

    def _download_next_images(self, prefix):
        """
        Shuffle s3 image indexes and iterating through it.
        Download batch_size images from s3, make T-shirt, create s3 urls
        and save it to redis. When s3 images end, shuffle and
        start iterating from the beginning.
        """
        server_indexes = []

        for i in range(BATCH_SIZE):
            server_indexes.append(self.server_images_index[self.current_image])

            self.current_image += 1
            if self.current_image >= MAX_IMAGES:
                self.current_image = 0
                random.shuffle(self.server_images_index)

        downloaded_images_files = []
        for server_index in server_indexes:
            downloaded_images_files.append(
                self._download_and_process_image(server_index))

        images_urls = self._make_urls(server_indexes)
        s = time.time()
        self._save_to_redis(downloaded_images_files, images_urls, prefix)
        # TODO: logging
        print(f'Transaction time: {time.time() - s:.3f}s', flush=True)

    def run(self):
        """
        Infinite images and urls updating. There are to alternating group to
        escape resources inconsistency. Stop updating then there are not
        new requests to main server(sync_file).
        """
        last_update = 0
        st_atime = 0
        prefix_alternates = ['a', 'b']
        step = 0

        while True:
            cur_time = time.time()
            if cur_time - last_update > UPDATE_DELTA and\
               cur_time - st_atime < UPDATE_DELTA * 2:
                last_update = time.time()
                prefix = prefix_alternates[step % 2]

                self._download_next_images(prefix)
                self.prefix_file.write_text(prefix)
                step += 1
                # TODO: logging
                print(f'Step {step}, downloading:'
                      f'{time.time() - last_update:.3f}s',
                      flush=True)
            else:
                time.sleep(0.5)
                st_atime = self.sync_file.stat().st_atime


if __name__ == '__main__':
    worker = Worker()
    worker.run()



