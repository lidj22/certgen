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

import generate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

is_mac = platform == "darwin"
is_linux = platform == "linux"

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'success')

def add_certificate_authority():
    if is_mac:
        subprocess.run(["security", "add-trusted-cert", "-d", "-r", "trustRoot", "-k", "/Library/Keychains/System.keychain", "./out/certificate-authority/CA.pem"])
    if is_linux:
        os.makedirs("/usr/local/share/ca-certificates/tmp", exist_ok=True)
        subprocess.run(["cp", "./out/test/certificate-authority/CA.pem", "/usr/local/share/ca-certificates/tmp/CA.crt"])
        subprocess.run(["update-ca-certificates"])
        time.sleep(1)
    logger.info("Added certificate authority.")

def remove_certificate_authority():
    if is_mac:
        subprocess.run(["security", "delete-certificate", "-c", "testCA", "-t"])
    if is_linux:
        subprocess.run(["rm", "-rf", "/usr/local/share/ca-certificates/tmp"])
        subprocess.run(["update-ca-certificates"])
    logger.info("Deleted certificate authority.")

def run_curl_test() -> bool:
    _is_curl_success = False
    try:
        result = subprocess.run(["curl", "https://localhost:443"], capture_output=True, text=True)
        if result.stdout=="success":
            logger.info("Passed curl test.")
            _is_curl_success = True
        else:
            logger.error("Failed curl test.")
    except Exception:
        logger.error(traceback.format_exc())
    finally:
        return _is_curl_success

def run_request_test() -> bool:
    _is_request_success = False
    try:
        os.environ["REQUESTS_CA_BUNDLE"] = f"{os.path.curdir}/out/test/certificate-authority/CA.pem"
        response = requests.get(
            "https://localhost:443",
            # verify=False,
        )
        if response.status_code == 200:
            logger.info("Passed requests test.")
            _is_request_success = True
        else:
            logger.error("Failed requests test.")
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        return _is_request_success

def main():

    if os.geteuid() != 0:
        logger.error("Root privileges is required to run this script.")
        exit(1)

    # generate certificates.
    generate.generate_certificate_authority()
    generate.generate_server_certificate()

    # add certificate authority
    add_certificate_authority()

    # load web server
    logger.info("Setting up HTTPS server on port 443.")
    httpd = HTTPServer(("localhost", 443), Handler)
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile="./out/test/servers/server.crt",
        keyfile="./out/test/servers/server.key",
        server_side=True,
    )
    servt = threading.Thread(target=httpd.serve_forever)
    servt.start()
    logger.info("HTTPS server setup complete.")

    # tests
    logger.info("Testing validity of server certificate induced by certificate authority...")
    pass_curl_test = run_curl_test()
    pass_request_test = run_request_test()

    remove_certificate_authority()

    # stop web server
    logger.info("Shutting down HTTPS server...")
    httpd.shutdown()
    servt.join()

    # resolve
    if pass_request_test and pass_curl_test:
        logger.info("Successfully validated certificate authority and cleaned everything up.")
    else:
        logger.error("Failed to validate certificate authority.")
        logger.error(f"Curl success status: {pass_curl_test}; Requests success status: {pass_request_test}.")
        raise requests.exceptions.SSLError

if __name__ == "__main__":
    main()