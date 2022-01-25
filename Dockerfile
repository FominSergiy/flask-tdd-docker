FROM python:3.9.5-slim-buster

# set workdir
WORKDIR /usr/src/app

# set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add the app
COPY . .

# run the container
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

