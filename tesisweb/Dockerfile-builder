FROM python:3.9.6-alpine

WORKDIR /usr/src/app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN apk update
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    postgresql-dev \
    && pip install --no-cache-dir psycopg2 \
    && pip install --no-cache-dir psycopg2-binary \
    && pip install --no-cache-dir Pillow \
    && apk del --no-cache .build-deps

RUN apk add libjpeg
RUN pip install -r requirements.txt

