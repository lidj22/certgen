#!/bin/sh

mkdir -p ./out

# CA configuration
openssl genrsa -out ./out/CA.key 2048
openssl req -x509 \
    -new \
    -nodes \
    -key ./out/CA.key \
    -sha256 -days 825 \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=testCA"\
    -out ./out/CA.pem
