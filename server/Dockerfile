FROM python:3.7-alpine

# zlib for pillow
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD python worker.py & gunicorn --bind 0.0.0.0:5000 --workers=4 app:app
