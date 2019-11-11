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
* Removed all the options except:

```diff
+ force_https_permanent: Uses 301 instead of 302 redirects.
+ referrer_policy: A string describing the referrer policy for the response.
+ session_cookie_secure: Forces the session cookie to only be sent over https. Disabled in debug mode.
+ session_cookie_http_only: Prevents JavaScript from reading the session cookie.
+ force_file_save: Prevents the user from opening a file download directly on >= IE 8
```

## Disclaimer

This is not an official Google *or* RDIL product, experimental or otherwise.

There is no silver bullet for web application security. Talisman can help, but security is more than just setting a few headers. Any public-facing web application should have a comprehensive approach to security.
