FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y build-essential
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get install -y zip
RUN pip install --upgrade pip
RUN pip install nose
RUN pip install redis

WORKDIR /sca_python
ADD . /sca_python
