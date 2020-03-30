FROM python:3.8

WORKDIR /web

RUN apt-get update && apt-get install -y gettext && rm -rf /var/cache/apt

COPY requirements.txt /requirements.txt
COPY requirements_dev.txt /requirements_dev.txt

RUN pip install -U pip; pip install -r /requirements_dev.txt
