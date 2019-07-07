from pathlib import Path
import os
import argparse
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool

logo = Image.open('logo_op.png')
max_images = 21979


def insert_logo(image, i):
    img_w, img_h = image.size

    offset = (img_w // 80 * 71, img_h // 30 * 29)
    image.paste(logo, offset, mask=logo.split()[3])
    image.save('images_with_logo/image_{}.png'.format(i))
    return image


def make_small_image(image, i, size):
    image = image.resize((size, size))
    image.save('small_images/image_{}.png'.format(i))
    return image


def process_image(img_path):
    try:
        num = int(img_path.name.split('.')[0].split('_')[1])
        img = Image.open(img_path)

        img = insert_logo(img, num)
        make_small_image(img, num, args.small_size)
    except:
        print(img_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_images', type=str, default='generated_images')
    parser.add_argument('--small_size', type=int, default=512)

    args = parser.parse_args()
    input_images = Path(args.input_images)

    with Pool(os.cpu_count()) as pool:
        list(tqdm(pool.imap(process_image, input_images.iterdir()),
             total=max_images))
    pool.close()

