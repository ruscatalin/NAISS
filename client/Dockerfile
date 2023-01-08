# Looks useless atm, better use a script / playwright instead of docker

FROM python:3.8.5-slim-buster

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y python-pip
RUN pip install beautifulsoup4

COPY . .
COPY ../server .
EXPOSE 7778

CMD python request_and_check.py