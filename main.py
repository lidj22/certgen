import logging
import subprocess

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("Starting script.")

subprocess.call("./scripts/generate.sh", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed credential generation stage.")

subprocess.run(["docker", "build", "-t", "cert-test", "."], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container build stage.")

subprocess.run(["docker", "run", "-d", "-p", "443:443", "--name", "cert-test", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Passed container run stage.")

subprocess.run(["curl", "https://localhost:443"])

subprocess.run(["docker", "stop", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Stopped container.")

subprocess.run(["docker", "container", "rm", "cert-test"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
logger.info("Removed container.")
