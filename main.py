import logging
import subprocess

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Starting script.")

subprocess.call("./scripts/generate.sh", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed credential generation stage.")

# add CA (mac)
subprocess.run(["security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", "/Library/Keychains/System.keychain", "./out/CA.pem"])
logger.info("Added test certificate authority.")

subprocess.run(["docker", "build", "-t", "cert-test", "."], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container build stage.")

subprocess.run(["docker", "run", "-d", "-p", "443:443", "--name", "cert-test", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container run stage.")

subprocess.run(["curl", "https://localhost:443"])

# remove CA (mac)
subprocess.run(["security", "delete-certificate", "-c", "special-name", "-t"])
logger.info("Deleted test certificate authority.")

subprocess.run(["docker", "stop", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Stopped container.")

subprocess.run(["docker", "container", "rm", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Removed container.")
