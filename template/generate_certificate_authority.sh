#!/bin/sh

mkdir -p {CA_DIR}

# CA configuration
openssl genrsa -out {CA_DIR}/CA.key 2048
openssl req -x509 \
    -new \
    -nodes \
    -key {CA_DIR}/CA.key \
    -sha256 -days {CA_VALID_DAYS} \
    -subj "/C={CA_COUNTRY}/ST={CA_STATE}/L={CA_LOC}/O={CA_ORG}/OU={CA_ORGU}/CN={CA_COMMON_NAME}"\
    -out {CA_DIR}/CA.pem
