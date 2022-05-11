FROM python:3.9.6-alpine AS builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt





FROM python:3.9.6-alpine

RUN mkdir -p /home/app

#con esto se crea un usuario llamado "app" y un grupo tambien llamado "app" en el contenedor
RUN addgroup -S app && adduser -S app -G app

#con esto se crean variables de entorno de las carpetas que se usaran para el proyecto de django
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME

#con esto se intalan las dependencias desde el builder
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
    && pip install --no-cache-dir djangorestframework \
    && pip install --no-cache-dir markdown \
    && pip install --no-cache-dir django-filter \
    && pip install --no-cache-dir django-cors-headers \
    && apk del --no-cache .build-deps
RUN apk add libjpeg
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

#con esto e copia el proyecto a la carpeta que fue creada con el usuario "app"
COPY . $APP_HOME

#con esto se le cambia tanto el usuario y el grupo al que pertenece la carpeta donde esta el proyecto
RUN chown -R app:app $APP_HOME

#con esto se cambia al usuario que creamos
USER app
