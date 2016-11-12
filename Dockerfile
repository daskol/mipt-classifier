FROM buildpack-deps:xenial

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 python3-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV FLASK_APP=miptclass.wsgi:app LANG=C.UTF-8 PYTHONPATH=/usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN pip install -e /usr/src/app
