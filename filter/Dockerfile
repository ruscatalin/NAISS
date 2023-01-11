FROM python:3.10-alpine as base

LABEL com.abhinavsingh.name="abhinavsingh/proxy.py" \
  com.abhinavsingh.description="⚡ Fast • 🪶 Lightweight • 0️⃣ Dependency • 🔌 Pluggable • \
  😈 TLS interception • 🔒 DNS-over-HTTPS • 🔥 Poor Man's VPN • ⏪ Reverse & ⏩ Forward • \
  👮🏿 \"Proxy Server\" framework • 🌐 \"Web Server\" framework • ➵ ➶ ➷ ➠ \"PubSub\" framework • \
  👷 \"Work\" acceptor & executor framework" \
  com.abhinavsingh.url="https://github.com/abhinavsingh/proxy.py" \
  com.abhinavsingh.vcs-url="https://github.com/abhinavsingh/proxy.py" \
  com.abhinavsingh.docker.cmd="docker run -it --rm -p 8899:8899 abhinavsingh/proxy.py" \
  org.opencontainers.image.source="https://github.com/abhinavsingh/proxy.py"

ENV PYTHONUNBUFFERED 1

ARG SKIP_OPENSSL
ARG PROXYPY_PKG_PATH

# COPY README.md /
# COPY $PROXYPY_PKG_PATH /

# RUN apk update && apk add make && apk add bash && apk add curl
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"

# RUN make lib-dep
# RUN pip install --upgrade pip && pip install tox
# RUN apk add git

# COPY proxy.py/requirements-release.txt .
# RUN pip install -r requirements-release.txt
# RUN rm requirements-release.txt

# COPY proxy.py/ /proxy.py/
# WORKDIR /proxy.py

RUN pip install --upgrade pip
RUN pip install beautifulsoup4
RUN pip install ecdsa
RUN pip install Flask
RUN pip install requests
COPY . .

# RUN apk add curl


# RUN pip install --upgrade pip && \
#   pip install \
#   --no-index \
#   # --find-links file:/// \
#   proxy.py && \
#   rm *.whl

# RUN pip install --upgrade pip && pip install proxy.py

# RUN ./write-scm-version.sh
# RUN make

# Use `--build-arg SKIP_OPENSSL=1` to disable openssl installation
# RUN if [[ -z "$SKIP_OPENSSL" ]]; then apk update && apk add openssl; fi
# RUN apk update && apk add openssl

EXPOSE 8899/tcp
# ENTRYPOINT ["proxy", "--hostname", "0.0.0.0", "--cert-file", "https-cert.pem", "--key-file", "https-key.pem"]
# ENTRYPOINT ["python", "-m", "proxy", "--hostname", "0.0.0.0", "--enable-reverse-proxy", "--plugins", "proxy.plugin.ReverseProxyPlugin"]
ENTRYPOINT [ "python", "reverse_proxy.py" ]
# ENTRYPOINT [ "curl", "http://127.0.0.1:7777/websites/clean/evilsig_clean_internal_png_index.html" ]

# CMD ["--cert-file https-cert.pem", "--key-file https-key.pem"]

# CMD [ \
#   # "--hostname=0.0.0.0" \
#   "--cert-file https-cert.pem" \
#   "--key-file https-key.pem" \
  # ]
