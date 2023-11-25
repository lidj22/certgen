import os
import subprocess
from typing import List
import yaml

GENERATE_CERTIFICATE_AUTHORITY_TEMPLATE = "./template/generate_certificate_authority.sh"
GENERATE_SERVER_CERTIFICATE_TEMPLATE = "./template/generate_server_certificate.sh"

EXT_FILE: str = """authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth, codeSigning, emailProtection
subjectAltName = {SUBJECT_ALT_NAMES}"""

def generate_ext_file(
        subject_alt_name_list: List[str]=["DNS:localhost"]
):
    return EXT_FILE.format(
        SUBJECT_ALT_NAMES=",".join(subject_alt_name_list)
    )

def generate_certificate_authority(
        site: str=None,
        ca_common_name: str=None,
        ca_country: str=None,
        ca_state: str=None,
        ca_loc: str=None,
        ca_org: str=None,
        ca_org_unit: str=None,
        ca_valid_days: int=None,
        regenerate: bool=False,
):
    
    script_dir = f"./out/{site}/scripts"
    os.makedirs(script_dir, exist_ok=True)
    script_path = f"{script_dir}/generate_certificate_authority.sh"

    with open(GENERATE_CERTIFICATE_AUTHORITY_TEMPLATE, "r", encoding="utf-8") as reader:
        template = reader.read()
    
    script = template.format(
        CA_DIR=f"./out/{site}/certificate-authority",
        CA_COMMON_NAME=ca_common_name,
        CA_COUNTRY=ca_country,
        CA_STATE=ca_state,
        CA_LOC=ca_loc,
        CA_ORG=ca_org,
        CA_ORGU=ca_org_unit,
        CA_VALID_DAYS=ca_valid_days,
    )

    if regenerate or not os.path.exists(script_path):
        with open(script_path, "w", encoding="utf-8") as writer:
            writer.write(script)
        subprocess.run(["chmod", "+x", script_path])
        subprocess.call(script_path)

def generate_server_certificate(
        site: str=None,
        common_name: str=None,
        country: str=None,
        state: str=None,
        loc: str=None,
        org: str=None,
        org_unit: str=None,
        valid_days: str=None,
        subject_alt_name_list: List[str]=["DNS:localhost"],
        regenerate: bool=False,
):
    script_dir = f"./out/{site}/scripts"
    os.makedirs(script_dir, exist_ok=True)
    script_path = f"{script_dir}/generate_{common_name}_certificate.sh"

    with open(GENERATE_SERVER_CERTIFICATE_TEMPLATE, "r", encoding="utf-8") as reader:
        template = reader.read()

    ext_file = generate_ext_file(subject_alt_name_list=subject_alt_name_list)
    script = template.format(
        CA_DIR=f"./out/{site}/certificate-authority",
        SERVER_DIR=f"./out/{site}/servers",
        COMMON_NAME=common_name,
        COUNTRY=country,
        STATE=state,
        LOC=loc,
        ORG=org,
        ORGU=org_unit,
        VALID_DAYS=valid_days,
        EXT_FILE=ext_file,
    )

    if regenerate or not os.path.exists(script_path):
        with open(script_path, "w", encoding="utf-8") as writer:
            writer.write(script)
        subprocess.run(["chmod", "+x", script_path])
        subprocess.call(script_path)

def generate_certificates_from_config(
        config_path: str="test-config.yaml",
        regenerate_certificates: bool=False,
        regenerate_certificate_authority: bool=False,
):
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(config_path)
    
    with open(config_path, "r", encoding="utf-8") as reader:
        config = yaml.safe_load(reader)
    
    site_name: str = config["site-name"]
    certificate_auth_config = config["certificate-authority"]
    server_configs = config["servers"]

    # generate ca files.
    ca_common_name = certificate_auth_config.get("common_name")
    ca_country = certificate_auth_config.get("country")
    ca_state = certificate_auth_config.get("state")
    ca_loc = certificate_auth_config.get("loc")
    ca_org = certificate_auth_config.get("org")
    ca_org_unit = certificate_auth_config.get("org_unit")
    ca_valid_days = certificate_auth_config.get("valid_days")
    generate_certificate_authority(
        site=site_name,
        ca_common_name=ca_common_name,
        ca_country=ca_country,
        ca_state=ca_state,
        ca_loc=ca_loc,
        ca_org=ca_org,
        ca_org_unit=ca_org_unit,
        ca_valid_days=ca_valid_days,
        regenerate=regenerate_certificate_authority,
    )

    # generate server files.
    for server in server_configs:
        common_name = server.get("common_name")
        country = server.get("country")
        state = server.get("state")
        loc = server.get("loc")
        org = server.get("org")
        org_unit = server.get("org_unit")
        valid_days = server.get("valid_days")
        subject_alt_names = server.get("subject_alt_names")
        generate_server_certificate(
            site=site_name,
            common_name=common_name,
            country=country,
            state=state,
            loc=loc,
            org=org,
            org_unit=org_unit,
            valid_days=valid_days,
            subject_alt_name_list=subject_alt_names,
            regenerate=regenerate_certificates,
        )
