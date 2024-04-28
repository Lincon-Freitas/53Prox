FROM alpine
# Metadata
LABEL maintainer="https://github.com/Lincon-Freitas"
LABEL version="1.0"
LABEL description="53Prox - DNS Proxy that translates queries over TLS."

RUN apk add --update --no-cache python3
WORKDIR /app

COPY config.json .
COPY server.py .

EXPOSE 53 53/udp

CMD ["python3", "server.py"]
