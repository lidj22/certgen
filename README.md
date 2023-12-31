# Certificate Authority Tests

Goals:

- Create a functional certificate authority
- Configurable CA and server certificate generation

| OS | Curl Works | Requests Works | Nginx Works |
| - | - | - | - |
| OSX | yes | yes | yes |
| Ubuntu 22 | yes | yes | yes |

## Usage

Generate certificates from config (e.g. `test.yaml`):
```sh
python generate.py --config ./config/test.yaml
```

Regenerate certificates:
```sh
python generate.py --regenerate ...
```
Regenerate CA:
```sh
python generate.py --regenerate-ca ...
```

### Test

Test the certificate generation process:
```sh
sudo python test.py
```

## Resources
All the tutorials and stack exchanges.
- [Create Your Own SSL Certificate Authority for Local HTTPS Development](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)
- [How to generate a self-signed SSL certificate using OpenSSL?](https://stackoverflow.com/a/41366949)
- [Root certificate authority works windows/linux but not mac osx](https://superuser.com/questions/762158/root-certificate-authority-works-windows-linux-but-not-mac-osx-malformed)
- [More strict Server Certificate handling in iOS 13 macOS 10.15](https://blog.nashcom.de/nashcomblog.nsf/dx/more-strict-server-certificate-handling-in-ios-13-macos-10.15.htm)
- [Never see localhost HTTPS warnings again](https://expeditedsecurity.com/blog/localhost-ssl-fix/)
- [Mac Users: Create Your Own Certificate Authority & Self Signed Certificate in Keychain Access](https://www.reddit.com/r/synology/comments/13vertq/mac_users_create_your_own_certificate_authority/)