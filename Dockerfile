FROM python:3-alpine

ARG MODE=production

RUN set -ex && \
    apk add --no-cache --virtual build-deps build-base musl-dev libffi-dev openssl-dev && \
    pip install pipenv && \
    mkdir /app

WORKDIR /app
ADD . /app

RUN set -ex && \
    pipenv install --system && \
    if [ "$MODE" = "development" ]; then pipenv install --system --dev; fi && \
    apk del build-deps

ENV PYTHONPATH=/app
