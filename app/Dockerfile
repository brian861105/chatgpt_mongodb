FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get -y install \
        wget\
        python3-pip \
        build-essential \
        libffi-dev \
        libssl-dev \
        && apt-get clean

WORKDIR /app
#COPY . /app

CMD ["/bin/bash"]