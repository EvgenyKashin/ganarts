# Generator 
Based on Nvidia [StyleGAN](https://github.com/NVlabs/stylegan)
## Docker
### GPU
```
sudo docker build -t digitman/tf_gan -f Dockerfile generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) digitman/tf_gan bash
```

### CPU
Currently it is not supported.
```
sudo docker build -t digitman/tf_gan_cpu -f Dockerfile.cpu generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) -p 8888:8888 digitman/tf_gan_cpu bash
jupyter notebook --port 8888 --ip 0.0.0.0 --allow-root
```
## Run image generation 
Upload local files(with model weights)to server:
```
rsync -av -e "ssh -p 32237" --exclude=".idea" --exclude=".git" ganarts root@ssh4.vast.ai:/root
```

In docker:
```
cd generator
python main.py --n_samples 64 --truncation_psi 0.7
```

## Quick S3 help
```
- pip install awscli
- aws configure (eu-central-1)
- aws s3 ls s3://ganarts
- aws s3 rb s3://ganarts --force
- aws s3 mb s3://ganarts
- aws s3 sync generated_images s3://ganarts/images/
- aws s3 sync s3://ganarts/images/ downloaded
```

## On weights converting
You should replace all NCHW layers with NHWC in 
https://github.com/NVlabs/stylegan/blob/master/training/networks_stylegan.py

I gave up in https://github.com/NVlabs/stylegan/blob/master/training/networks_stylegan.py#L514

And if it works, you should convert changed layers weights (https://stackoverflow.com/questions/39555256/tensorflow-how-can-i-assign-numpy-pre-trained-weights-to-subsections-of-graph)

ONNX (https://github.com/onnx/tensorflow-onnx) can't convert such difficult architecture.
