#!/bin/sh

mkdir -p ./out/test/servers

# server certificate
openssl genrsa -out ./out/test/servers/server.key 2048
openssl req -new -key ./out/test/servers/server.key \
    -subj "/C=NA/ST=NA/L=NA/O=org/OU=orgunit/CN=testServer"\
    -out ./out/test/servers/server.csr

# IP:${your-ip-address}
echo "authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection
subjectAltName = DNS:localhost,DNS:testServer" | openssl x509 -req -in ./out/test/servers/server.csr \
    -CA ./out/test/certificate-authority/CA.pem \
    -CAkey ./out/test/certificate-authority/CA.key \
    -CAcreateserial \
    -out ./out/test/servers/server.crt \
    -days 825 \
    -sha256 \
    -extfile /dev/stdin > /dev/null