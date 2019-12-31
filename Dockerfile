FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

COPY ./requirements.txt /var/www/requirements.txt

RUN apk update --no-cache \
    && apk add --no-cache --virtual .build-deps \
    python3 python3-dev py3-pip \
    g++ make libffi-dev openssl-dev \
    ##
    && pip install -r /var/www/requirements.txt \
    && apk del .build-deps

ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /var/www/app/static
