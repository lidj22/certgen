import logging
import os
import subprocess
from sys import platform
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Starting script.")
is_mac = platform == "darwin"
is_linux = platform == "linux"

subprocess.call("./scripts/generate.sh")
logger.info("Passed credential generation stage.")

# add certificate authority
if is_mac:
    subprocess.run(["security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", "/Library/Keychains/System.keychain", "./out/CA.pem"])
if is_linux:
    os.makedirs("/usr/local/share/ca-certificates/tmp", exist_ok=True)
    subprocess.run(["mkdir", "-p", "/usr/local/share/ca-certificates/tmp"])
    subprocess.run(["cp", "./out/CA.pem", "/usr/local/share/ca-certificates/tmp/CA.crt"])
    subprocess.run(["update-ca-certificates"])
    time.sleep(1)
logger.info("Added certificate authority.")

subprocess.run(["docker", "build", "-t", "cert-test", "."])
logger.info("Passed container build stage.")
time.sleep(1)

subprocess.run(["docker", "run", "-d", "-p", "443:443", "--name", "cert-test", "cert-test"])
logger.info("Passed container run stage.")
time.sleep(1)

subprocess.run(["curl", "https://localhost:443"])

# remove certificate authority and clean up
if is_mac:
    subprocess.run(["security", "delete-certificate", "-c", "special-name", "-t"])
if is_linux:
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/tmp"])
    subprocess.run(["update-ca-certificates"])
logger.info("Deleted certificate authority.")

subprocess.run(["docker", "stop", "cert-test"])
logger.info("Stopped container.")

subprocess.run(["docker", "container", "rm", "cert-test"])
logger.info("Removed container.")
