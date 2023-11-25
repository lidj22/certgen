import logging
import requests
import os
import subprocess
from sys import platform
import time
import traceback

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Starting script.")
is_mac = platform == "darwin"
is_linux = platform == "linux"
is_success = False

subprocess.call("./scripts/generate.sh")
logger.info("Passed credential generation stage.")

# add certificate authority
if is_mac:
    subprocess.run(["security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", "/Library/Keychains/System.keychain", "./out/CA.pem"])
if is_linux:
    os.makedirs("/usr/local/share/ca-certificates/tmp", exist_ok=True)
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

logger.info("Testing validity of server certificate induced by certificate authority...")
try:
    response = requests.get("https://localhost:443")
    if response.status_code == 200:
        is_success = True
except Exception as e:
    logger.error(traceback.format_exc())
# subprocess.run(["curl", "https://localhost:443"])

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

# resolve
if is_success:
    logger.info("Successfully validated certificate authority and cleaned everything up.")
else:
    logger.error("Failed to validate certificate authority.")
    raise requests.exceptions.SSLError
