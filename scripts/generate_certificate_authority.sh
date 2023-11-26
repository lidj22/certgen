#!/bin/sh

mkdir -p ./out/test/certificate-authority

# CA configuration
openssl genrsa -out ./out/test/certificate-authority/CA.key 2048
openssl req -x509 \
    -new \
    -nodes \
    -key ./out/test/certificate-authority/CA.key \
    -sha256 -days 825 \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=testCA"\
    -out ./out/test/certificate-authority/CA.pem
