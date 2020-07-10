FROM ubuntu:18.04

ARG UNAME=celeryuser
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update

RUN apt-get install -y python3-pip
RUN apt-get install -y python3-distutils


RUN apt-get install -y \
    git \
    python3-pip \
    cmake


RUN apt-get install -y \
    autoconf \
    autotools-dev

RUN echo "y" | apt install python-psycopg2
RUN echo "y" | apt install libpq-dev python-dev
RUN echo "y" | apt install npm
RUN npm install -g load-test

COPY ./requirements.txt /scripts/
RUN pip3 install --no-cache-dir -r /scripts/requirements.txt

USER $UNAME

WORKDIR /applications/