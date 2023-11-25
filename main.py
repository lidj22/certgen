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
is_requests_success = False
is_curl_success = False

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'success')

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
httpd = HTTPServer(("localhost", 443), Handler)
httpd.socket = ssl.wrap_socket(
    httpd.socket,
    certfile="./out/server.crt",
    keyfile="./out/server.key",
    server_side=True,
)
servt = threading.Thread(target=httpd.serve_forever)
servt.start()
logger.info("HTTPS server setup complete.")

# test phase
logger.info("Testing validity of server certificate induced by certificate authority...")

# curl test
try:
    result = subprocess.run(["curl", "https://localhost:443"], capture_output=True, text=True)
    if result.stdout=="success":
        logger.info("Passed curl test.")
        is_curl_success = True
    else:
        logger.error("Failed curl test.")
except Exception as e:
    logger.error(traceback.format_exc())

# request test
try:
    response = requests.get("https://localhost:443")
    if response.status_code == 200:
        logger.info("Passed requests test.")
        is_requests_success = True
    else:
        logger.error("Failed requests test.")
except Exception as e:
    logger.error(traceback.format_exc())

# remove certificate authority and clean up
if is_mac:
    subprocess.run(["security", "delete-certificate", "-c", "testCA", "-t"])
if is_linux:
    subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/tmp"])
    subprocess.run(["update-ca-certificates"])
logger.info("Deleted certificate authority.")

# stop web server
logger.info("Shutting down HTTPS server...")
httpd.shutdown()
servt.join()

# resolve
if is_requests_success and is_curl_success:
    logger.info("Successfully validated certificate authority and cleaned everything up.")
else:
    logger.error("Failed to validate certificate authority.")
    logger.error(f"Curl success status: {is_curl_success}; Requests success status: {is_requests_success}.")
    raise requests.exceptions.SSLError
