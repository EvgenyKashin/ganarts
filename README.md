# Ganarts

## Generator 
### Docker
#### GPU
sudo docker build -t digitman/tf_gan -f docker/generator/Dockerfile generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) digitman/tf_gan bash

#### CPU
sudo docker build -t digitman/tf_gan_cpu -f docker/generator/Dockerfile.cpu generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) -p 8888:8888 digitman/tf_gan_cpu bash
jupyter notebook --port 8888 --ip 0.0.0.0 --allow-root # without -u option

### Run generation 
rsync -av -e "ssh -p 28187" --exclude=".idea" ganarts root@ssh4.vast.ai:/root # sync local files with server
In docker:
cd generator; python main.py

Generating 1024 images:
- ~8Gb GPU memory for batch size 16
- 256 seconds
- ~ $0.02
- 790 Mb on disk


### Upload to S3
- pip install awscli
- aws configure (eu-central-1)
- aws s3 ls s3://ganarts
- aws s3 rb s3://ganarts --force
- aws s3 mb s3://ganarts
- aws s3 sync generated_images s3://ganarts/images/
- aws s3 sync s3://ganarts/images/ downloaded
## Deploy
- cpu: layers converting is needed
- gpu: high renting cost
- s3: generating on gpu server, save to s3, serve on cpu server
 
### On converting weights
You should replace all NCHW layers with NHWC in 
https://github.com/NVlabs/stylegan/blob/master/training/networks_stylegan.py

I gave up in https://github.com/NVlabs/stylegan/blob/master/training/networks_stylegan.py#L514

And if it works, you should convert changed layers weights (https://stackoverflow.com/questions/39555256/tensorflow-how-can-i-assign-numpy-pre-trained-weights-to-subsections-of-graph)

ONNX (https://github.com/onnx/tensorflow-onnx) can't convert such difficult architecture.

### GPU deployment
https://medium.com/@rupak.thakur/aws-vs-paperspace-vs-floydhub-choosing-your-cloud-gpu-partner-350150606b39
- Hetzner (https://www.hetzner.com/) don't have available GPU servers now
- AWS ~$1/hr
- Others - $0.5/hr but limit on computing in a month

### S3
- 60 * 24 * 9 = 12960 images (1 image in minute) - should be generated in a day
