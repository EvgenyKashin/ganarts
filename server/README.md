# Server
## Docker
```
sudo docker build -t flask_server -f Dockerfile .
sudo docker run -it --rm -p 5000:5000 flask_server
sudo docker run redis
```
## Running
### S3 configuration:
```
export AWSAccessKeyId=...
export AWSSecretKey=...
```
### Gunicorn
```
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 --workers=4 app:app
```
### RPS test
```
- wrk -t12 -c100 -d60s http://127.0.0.1:5000
```

## Backend evolution
From 40 rps to 600rps locally:
- downloading and processing images from s3 in main thread each n seconds - baseline
- gunicron
- downloading in threads/process 
- background images downloading at separate folder on disk
- background images downloading in redis - current solution
