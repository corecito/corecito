FROM python:3.8.2-slim-buster

RUN apt-get update
RUN apt-get -y install gcc

RUN pip install --upgrade pip
RUN pip install pyyaml
RUN pip install cryptocom.exchange
RUN pip install python-binance

ADD --chown=777 ./ /root/corecito

WORKDIR /root/corecito
