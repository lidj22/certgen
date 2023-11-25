#!/bin/sh

mkdir -p ./out

# CA configuration
openssl genrsa -out ./out/CA.key 2048
openssl req -x509 \
    -new \
    -nodes \
    -key ./out/CA.key \
    -sha256 -days 365 \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=special-name"\
    -out ./out/CA.pem

# server certificate
openssl genrsa -out ./out/server.key 2048
openssl req -new -key ./out/server.key \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=special-name"\
    -out ./out/server.csr
    
echo "extendedKeyUsage = serverAuth
subjectAltName=DNS:localhost" | openssl x509 -req -in ./out/server.csr \
    -CA ./out/CA.pem \
    -CAkey ./out/CA.key \
    -CAcreateserial \
    -out ./out/server.crt \
    -days 825 \
    -sha256 \
    -extfile /dev/stdin > /dev/null