#!/bin/sh

# server certificate
openssl genrsa -out ./out/server.key 2048
openssl req -new -key ./out/server.key \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=testServer"\
    -out ./out/server.csr

# IP:${your-ip-address}
echo "authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection
subjectAltName = DNS:localhost,DNS:testServer" | openssl x509 -req -in ./out/server.csr \
    -CA ./out/CA.pem \
    -CAkey ./out/CA.key \
    -CAcreateserial \
    -out ./out/server.crt \
    -days 825 \
    -sha256 \
    -extfile /dev/stdin > /dev/null