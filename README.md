# Ganarts
This T-shirt does not exist

## Generator 
### Docker
#### GPU
```
sudo docker build -t digitman/tf_gan -f docker/generator/Dockerfile generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) digitman/tf_gan bash
```

#### CPU
```
sudo docker build -t digitman/tf_gan_cpu -f docker/generator/Dockerfile.cpu generator
sudo docker run -it --rm -v `pwd`/generator:/stylegan -u $(id -u):$(id -g) -p 8888:8888 digitman/tf_gan_cpu bash
jupyter notebook --port 8888 --ip 0.0.0.0 --allow-root # without -u option
```
### Run generation 
```
rsync -av -e "ssh -p 32237" --exclude=".idea" --exclude=".git" ganarts root@ssh4.vast.ai:/root # sync local files with server
```

In docker:
```
cd generator
python main.py --n_samples 64 --truncation_psi 0.7
```

### Upload to S3
```
- pip install awscli
- aws configure (eu-central-1)
- aws s3 ls s3://ganarts
- aws s3 rb s3://ganarts --force
- aws s3 mb s3://ganarts
- aws s3 sync generated_images s3://ganarts/images/
- aws s3 sync s3://ganarts/images/ downloaded
```

#### Store now
- 21981 images
- 46Gb
- weights.pkl ~300mb

## Prices
Generating 1024 images:
- ~8Gb GPU memory with batch size 16
- 256 seconds
- ~ $0.02 to compute (vast.ai)
- 790 Mb on disk
- ~$0.025/1Gb month to store (aws s3)
- ~$0.09/1Gb transfer from s3
- ~$0.01 per 1000 PUT/SELECT requests

## Deploy options
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

## Server
### Running

```
export AWSAccessKeyId=...
export AWSSecretKey=...
python server/app.py
```
### Gunicorn
```
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers=1 app:app
```
### Testing rps
```
- time python multiple_sync_request_threaded.py -nr 1000 -nt 20
- wrk -t12 -c100 -d60s http://127.0.0.1:5000
- python -c "import app; app.benchmark()"
```
Results:
- baseline: 100,144,100ms lat, 23,16,47rps, timeouts 193, 193, 289, benchmark 14, 13, 13
- keep t-shirt image and logo in memory, drop one redundant loop: benchmark 13.7, 12.7, 12.3
- parallel image downloading-processing(not tested well): 125,133,113ms lat, 345,285,255rps, timeouts 384x3, benchmark 8.3, 9, 6.7
- parallel image downloading-processing (Threads - no bug): 169ms lat, 14 rps, benchmark 14, 14, 13
Pool - truncated images, non blocking code problem. Tread pool - error in images order.
Raw thread very slow. Raw thread with separate session for each thread - error.