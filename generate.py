import os
import subprocess

EXT_FILE: str = """authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection
subjectAltName = DNS:localhost"""

def generate_certificate_authority():
    os.makedirs("./out/scripts", exist_ok=True)
    script_path = "./out/scripts/generate_certificate_authority.sh"

    with open("template/generate_certificate_authority.sh", "r", encoding="utf-8") as reader:
        template = reader.read()
    
    script = template.format(
        CA_DIR="./out/test/certificate-authority",
        CA_COMMON_NAME="testCA",
        CA_COUNTRY="NA",
        CA_STATE="NA",
        CA_LOC="NA",
        CA_ORG="org",
        CA_ORGU="orgu",
        CA_VALID_DAYS=825,
    )

    with open(script_path, "w", encoding="utf-8") as writer:
        writer.write(script)
    subprocess.run(["chmod", "+x", script_path])
    subprocess.call(script_path)

def generate_server_certificate():
    os.makedirs("./out/scripts", exist_ok=True)
    script_path = "./out/scripts/generate_server_certificate.sh"

    with open("./template/generate_server_certificate.sh", "r", encoding="utf-8") as reader:
        template = reader.read()

    script = template.format(
        CA_DIR="./out/test/certificate-authority",
        SERVER_DIR="./out/test/servers",
        COMMON_NAME="testServer",
        COUNTRY="NA",
        STATE="NA",
        LOC="NA",
        ORG="org",
        ORGU="orgu",
        VALID_DAYS=825,
        EXT_FILE=EXT_FILE,
    )

    with open(script_path, "w", encoding="utf-8") as writer:
        writer.write(script)

    subprocess.run(["chmod", "+x", script_path])
    subprocess.call(script_path)
