FROM tensorflow/tensorflow:latest-gpu-py3-jupyter

RUN apt install -y rsync \
                   htop \
                   wget

RUN pip install pillow==5.4.1 \
                requests \
                tqdm \
                scipy

RUN mkdir stylegan
WORKDIR /stylegan