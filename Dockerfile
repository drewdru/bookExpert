FROM ubuntu:16.04
USER root
RUN apt update && \
    apt -y install wget build-essential python build-essential python3 \
    python3-dev python3-pip python3-venv python-dev graphviz 
RUN mkdir /code
WORKDIR /code
ADD . /code/
ADD requirements.txt /code/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install wheel
