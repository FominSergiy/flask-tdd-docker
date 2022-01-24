FROM python:3.9.5-slim-buster

# set workdir
WORKDIR /usr/src/app

# set env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add the app
COPY . .

# run the container
CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]

