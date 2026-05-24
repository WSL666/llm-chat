FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /apps/comfyui-api
COPY ./requirements.txt .
COPY ./debian.sources /etc/apt/sources.list.d/debian.sources
RUN mkdir /apps/logs && \
    apt-get update && apt-get install ffmpeg libsm6 libxext6 libgl1 -y && \
    pip install -r requirements.txt --default-timeout=5000