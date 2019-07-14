# Ganarts
This T-shirt does not exist.

Consist of [generator](generator)(based on StyleGAN) and 
[server](server)(flask + gunicorn + redis + s3).

## Deploy options
- cpu: layers converting is needed(NCHW -> NHWC)
- gpu: high renting cost
- s3(current): generating on gpu server, save to s3, serve on cpu server

Generator generates images, makes preprocessing and uploads to s3.
Backend worker downloads images and saves to redis each n seconds
 in one transaction. Main server gets 9 images 
 and urls of full size s3 images from redis and serves it to clients.

## EC2
- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/compose/install/
- git clone https://github.com/EvgenyKashin/ganarts.git
- create .env with s3 access keys
- sudo docker-compose up -d
