# GanArts
This T-shirt does not exist.

Images are generated with [StyleGAN](https://github.com/NVlabs/stylegan) neural network, 
trained on 40,000 images of modern art. The training process 
takes 3 days on 4x1080ti GPU. Every 30 seconds there are 9 new images, 
and the old ones are deleted. To print these images, 
use specialized sites(place for your ad). To increase the resolution, 
you can use a [super resolution](http://waifu2x.udp.jp) (increase the image size from 1024px to 2048px).

<img src="img/demo.gif">

Repo consist of [generator](generator)(based on StyleGAN) and 
[server](server)(flask + gunicorn + redis + s3).
## Deploy options
- cpu: layers converting is needed(NCHW -> NHWC)
- gpu: high renting cost
- s3(current): generating on gpu server, save to s3, serve on cpu server

Generator generates images, makes preprocessing and uploads to s3.
Backend worker downloads images and saves to redis each n seconds
 in one transaction. Main server gets 9 images 
 and urls of full-size images(on s3) from redis and serves these to clients.

## EC2
- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/compose/install/
- git clone https://github.com/EvgenyKashin/ganarts.git
- create .env with s3 access keys
- sudo docker-compose up -d
