FROM python:3.12.2-slim-bookworm

ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /home/callisto && \
    mkdir /home/callisto/CHZZK-VOD && \
    mkdir /home/callisto/plugins

COPY requirements.txt /home/callisto
COPY callisto.py /home/callisto
COPY /plugins/chzzk.py /home/callisto/plugins

RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install -y ffmpeg && \
    ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    pip3 install -r /home/callisto/requirements.txt

CMD ["python3", "/home/callisto/callisto.py"]