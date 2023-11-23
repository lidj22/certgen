import logging
import os
import subprocess
from sys import platform

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Starting script.")
is_mac = platform == "darwin"
is_linux = platform == "linux"

subprocess.call("./scripts/generate.sh", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed credential generation stage.")

# add certificate authority
if is_mac:
    subprocess.run(["security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", "/Library/Keychains/System.keychain", "./out/CA.pem"])
    logger.info("Added test certificate authority.")
if is_linux:
    os.makedirs("/usr/local/share/ca-certificates/tmp", exist_ok=True)
    subprocess.run(["mkdir", "-p", "/usr/local/share/ca-certificates/tmp"])
    subprocess.run(["cp", "./out/CA.pem", "/usr/local/share/ca-certificates/tmp/CA.crt"])
    subprocess.run(["update-ca-certificates"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

subprocess.run(["docker", "build", "-t", "cert-test", "."], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container build stage.")

subprocess.run(["docker", "run", "-d", "-p", "443:443", "--name", "cert-test", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container run stage.")

subprocess.run(["curl", "https://localhost:443"])

# remove certificate authority and clean up
if is_mac:
    subprocess.run(["security", "delete-certificate", "-c", "special-name", "-t"])
    logger.info("Deleted test certificate authority.")
if is_linux:
    subprocess.run(["update-ca-certificates"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/tmp"])

subprocess.run(["docker", "stop", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Stopped container.")

subprocess.run(["docker", "container", "rm", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Removed container.")
