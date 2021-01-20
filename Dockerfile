FROM microweb10/corecito_python:3.8.2

ADD --chown=777 ./ /root/corecito

WORKDIR /root/corecito
