FROM python:3.10-alpine as base

RUN pip install --upgrade pip
RUN pip install beautifulsoup4
RUN pip install ecdsa
RUN pip install Flask
RUN pip install requests
COPY . .

EXPOSE 8899/tcp

ENTRYPOINT [ "python", "reverse_proxy.py" ]
