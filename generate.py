import subprocess

def generate_certificate_authority():
    subprocess.call("./scripts/generate_certificate_authority.sh")

def generate_server_certificate():
    subprocess.call("./scripts/generate_server_certificate.sh")

