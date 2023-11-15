FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . /app

ENV PROJECT_NAME=movies
ENV REDIS_HOST=cache
ENV REDIS_PORT=6379
ENV ELASTIC_HOST=elasticsearch
ENV ELASTIC_PORT=9200
