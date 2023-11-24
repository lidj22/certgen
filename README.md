# Certificate Authority Tests

Project Goal: create a functional certificate authority

| OS | Works |
| - | - |
| OSX | no |
| Ubuntu 22 | yes |

## Usage
Install [Docker](https://docs.docker.com/engine/install/).

```sh
sudo python main.py
```
At the `curl` stage, the expected output should resemble the nginx welcome page.

## Other
All the tutorials and stack exchanges.
- [Create Your Own SSL Certificate Authority for Local HTTPS Development](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)
- [How to generate a self-signed SSL certificate using OpenSSL?](https://stackoverflow.com/a/41366949)
- [Root certificate authority works windows/linux but not mac osx](https://superuser.com/questions/762158/root-certificate-authority-works-windows-linux-but-not-mac-osx-malformed)
- [More strict Server Certificate handling in iOS 13 macOS 10.15](More strict Server Certificate handling in iOS 13 macOS 10.15)