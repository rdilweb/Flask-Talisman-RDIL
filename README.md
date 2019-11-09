# Flask-Talisman-RDIL

A fork of [Flask-Talisman](https://github.com/GoogleCloudPlatform/Flask-Talisman) with certain changes to better fit my backend server.

## Changelog

Because the license requires this, I will put the change log here:

* Removed files:
  * `.travis.yml`
  * `CONTRIBUTING.md`
  * `noxfile.py`
  * `README.rst` - replaced with this file (`README.md`)
* Removed the example app
* **Dropped Python 2 support**
* Added Gitpod configuration and Dockerfile
* Cleaned up `setup.py`
* Removed Google's content security policy, this is for a backend!
* Removed content security policies in general
* Removed force `HTTPS` because our hosting provider has SSL
* Removed nonce stuff
* HSTS was removed

## Disclaimer

This is not an official Google product, experimental or otherwise.

There is no silver bullet for web application security. Talisman can help, but security is more than just setting a few headers. Any public-facing web application should have a comprehensive approach to security.
