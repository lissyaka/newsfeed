FROM python:2.7

EXPOSE 8888

RUN apt-get update

RUN mkdir -p /app
WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements.txt
