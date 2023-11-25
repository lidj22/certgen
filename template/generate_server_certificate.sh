#!/bin/sh

mkdir -p {SERVER_DIR}

# server certificate
openssl genrsa -out {SERVER_DIR}/server.key 2048
openssl req -new -key {SERVER_DIR}/server.key \
    -subj "/C={COUNTRY}/ST={STATE}/L={LOC}/O={ORG}/OU={ORGU}/CN={COMMON_NAME}"\
    -out {SERVER_DIR}/server.csr

# IP:$(your-ip-addr)
echo "{EXT_FILE}" | openssl x509 -req -in {SERVER_DIR}/server.csr \
    -CA {CA_DIR}/CA.pem \
    -CAkey {CA_DIR}/CA.key \
    -CAcreateserial \
    -out {SERVER_DIR}/server.crt \
    -days {VALID_DAYS} \
    -sha256 \
    -extfile /dev/stdin > /dev/null