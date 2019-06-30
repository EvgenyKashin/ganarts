import pickle
from pathlib import Path
import argparse
import time
import numpy as np
import PIL.Image
import dnnlib.tflib as tflib

image_path = Path('generated_images')

tflib.init_tf()
image_path.mkdir(exist_ok=True)
is_cpu = False

with open('weights.pkl', 'rb') as f:
    _G, _D, Gs = pickle.load(f)


def generate_images(n_samples, batch_size, start_from):
    start_time = time.time()
    for ep in range(n_samples // batch_size):
        latents = np.random.rand(batch_size, Gs.input_shape[1])
        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True,
                        output_transform=fmt, is_cpu=is_cpu)

        for i in range(batch_size):
            filename = image_path / 'image_{}.png'.format(start_from +
                                                          ep * batch_size + i)
            PIL.Image.fromarray(images[i], 'RGB').save(filename)

    print('Done, {:.1f} seconds'.format(time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_samples', type=int, default=1024)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--start_from', type=int, default=0)

    args = parser.parse_args()
    generate_images(args.n_samples, args.batch_size, args.start_from)


