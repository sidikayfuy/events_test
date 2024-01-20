FROM python:3.10

RUN apt-get update
RUN apt-get install -y python3-dev

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENV DJANGO_SETTINGS_MODULE=events_test.settings
