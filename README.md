# Ganarts

## Generator 
### Docker
#### GPU
sudo docker build -t digitman/tf_gan -f docker/generator/Dockerfile generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) digitman/tf_gan bash

#### CPU
sudo docker build -t digitman/tf_gan_cpu -f docker/generator/Dockerfile.cpu generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) digitman/tf_gan_cpu bash

## Deploy
- cpu: layers converting is needed
- gpu: high renting cost
- s3: generating on gpu server, save to s3, serve on cpu server
 
### On converting weights
You should replace all NCHW layers with NHWC in 
https://github.com/NVlabs/stylegan/blob/master/training/networks_stylegan.py

And if it works, you should convert changed layers weights (https://stackoverflow.com/questions/39555256/tensorflow-how-can-i-assign-numpy-pre-trained-weights-to-subsections-of-graph)

### GPU deployment
https://medium.com/@rupak.thakur/aws-vs-paperspace-vs-floydhub-choosing-your-cloud-gpu-partner-350150606b39
- Hetzner (https://www.hetzner.com/) don't have available GPU servers now
- AWS ~$1/hr
- Others - $0.5/hr but limit on computing in a month

### S3
- 60 * 24 * 9 = 12960 images (1 image in minute) - should be generated in a day
