FROM ubuntu:20.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV TERM xterm-256color

WORKDIR /ohdo2

COPY . /ohdo2/

RUN apt update
RUN apt install -y curl jq python3-pip
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN pip3 install rest3client mpcurses
