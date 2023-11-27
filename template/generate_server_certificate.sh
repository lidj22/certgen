#!/bin/sh

mkdir -p {SERVER_DIR}

# server certificate
openssl genrsa -out {SERVER_DIR}/{COMMON_NAME}.key 2048
openssl req -new -key {SERVER_DIR}/{COMMON_NAME}.key \
    -subj "/C={COUNTRY}/ST={STATE}/L={LOC}/O={ORG}/OU={ORGU}/CN={COMMON_NAME}"\
    -out {SERVER_DIR}/{COMMON_NAME}.csr

# IP:$(your-ip-addr)
echo "{EXT_FILE}" | openssl x509 -req -in {SERVER_DIR}/{COMMON_NAME}.csr \
    -CA {CA_DIR}/CA.pem \
    -CAkey {CA_DIR}/CA.key \
    -CAcreateserial \
    -out {SERVER_DIR}/{COMMON_NAME}.crt \
    -days {VALID_DAYS} \
    -sha256 \
    -extfile /dev/stdin > /dev/null

# permissions
chmod 600 {SERVER_DIR}/{COMMON_NAME}.key
chmod 600 {SERVER_DIR}/{COMMON_NAME}.csr
chmod 600 {SERVER_DIR}/{COMMON_NAME}.crt