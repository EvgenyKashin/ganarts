import pickle
from pathlib import Path
import numpy as np
import PIL.Image
import dnnlib.tflib as tflib

n_samples = 9
image_path = Path('generated_images')

tflib.init_tf()
image_path.mkdir(exist_ok=True)

with open('weights.pkl', 'rb') as f:
    _G, _D, Gs = pickle.load(f)

import pdb;pdb.set_trace()

latents = np.random.rand(n_samples, Gs.input_shape[1])
fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True,
                output_transform=fmt, is_cpu=True)

for i in range(n_samples):
    filename = image_path / 'image_{}.png'.format(i)
    PIL.Image.fromarray(images[i], 'RGB').save(filename)
