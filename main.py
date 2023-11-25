from http.server import SimpleHTTPRequestHandler, HTTPServer
import ssl
import threading

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

class SimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()

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

# load web server
logger.info("Setting up HTTPS server on port 443.")
httpd = HTTPServer(("localhost", 443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile="./out/server.crt",
    keyfile="./out/server.key",
    server_side=True,
)
servt = threading.Thread(target=httpd.serve_forever)
servt.start()
logger.info("HTTPS server setup complete.")

logger.info("Testing validity of server certificate induced by certificate authority...")
try:
    response = requests.get("https://localhost:443")
    if response.status_code == 200:
        is_success = True
except Exception as e:
    logger.error(traceback.format_exc())

# remove certificate authority and clean up
if is_mac:
    subprocess.run(["security", "delete-certificate", "-c", "special-name", "-t"])
if is_linux:
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/tmp"])
    subprocess.run(["update-ca-certificates"])
logger.info("Deleted certificate authority.")

# stop web server
logger.info("Shutting down HTTPS server...")
httpd.shutdown()
servt.join()

# resolve
if is_success:
    logger.info("Successfully validated certificate authority and cleaned everything up.")
else:
    logger.error("Failed to validate certificate authority.")
    raise requests.exceptions.SSLError
