# The server is hosting the websites inside website/websites
# The websites are transmitted to the client via TLS
# Also, the websites are transmitted to the filter as well via TLS

FROM python:3.8.5-slim-buster
COPY website .
EXPOSE 7777

# CMD python -m http.server 7777
ENTRYPOINT [ "python", "-m", "http.server", "7777" ]
