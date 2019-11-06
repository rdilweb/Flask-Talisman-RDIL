# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import OrderedDict

import flask
from six import iteritems, string_types


DENY = 'DENY'
SAMEORIGIN = 'SAMEORIGIN'
ALLOW_FROM = 'ALLOW-FROM'
ONE_YEAR_IN_SECS = 31556926

DEFAULT_REFERRER_POLICY = 'strict-origin-when-cross-origin'

DEFAULT_FEATURE_POLICY = {
}

NONCE_LENGTH = 16


class Talisman(object):
    """
    Talisman is a Flask extension for HTTP security headers.
    """

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(
            self,
            app,
            feature_policy=DEFAULT_FEATURE_POLICY,
            force_https_permanent=False,
            force_file_save=False,
            frame_options=SAMEORIGIN,
            frame_options_allow_from=None,
            strict_transport_security=True,
            strict_transport_security_preload=False,
            strict_transport_security_max_age=ONE_YEAR_IN_SECS,
            strict_transport_security_include_subdomains=True,
            referrer_policy=DEFAULT_REFERRER_POLICY,
            session_cookie_secure=True,
            session_cookie_http_only=True
        ):
        """
        Initialization.

        Args:
            app: A Flask application.
            feature_policy: A string or dictionary describing the
                feature policy for the response.
            force_https: Redirects non-http requests to https, disabled in
                debug mode.
            force_https_permanent: Uses 301 instead of 302 redirects.
            frame_options: Sets the X-Frame-Options header, defaults to
                SAMEORIGIN.
            frame_options_allow_from: Used when frame_options is set to
                ALLOW_FROM and is a string of domains to allow frame embedding.
            strict_transport_security: Sets HSTS headers.
            strict_transport_security_preload: Enables HSTS preload. See
                https://hstspreload.org.
            strict_transport_security_max_age: How long HSTS headers are
                honored by the browser.
            strict_transport_security_include_subdomain: Whether to include
                all subdomains when setting HSTS.
            referrer_policy: A string describing the referrer policy for the
                response.
            session_cookie_secure: Forces the session cookie to only be sent
                over https. Disabled in debug mode.
            session_cookie_http_only: Prevents JavaScript from reading the
                session cookie.
            force_file_save: Prevents the user from opening a file download
                directly on >= IE 8

        See README.rst for a detailed description of each option.
        """
        if isinstance(feature_policy, dict):
            self.feature_policy = OrderedDict(feature_policy)
        else:
            self.feature_policy = feature_policy
        self.force_https_permanent = force_https_permanent

        self.frame_options = frame_options
        self.frame_options_allow_from = frame_options_allow_from

        self.strict_transport_security = strict_transport_security
        self.strict_transport_security_preload = \
            strict_transport_security_preload
        self.strict_transport_security_max_age = \
            strict_transport_security_max_age
        self.strict_transport_security_include_subdomains = \
            strict_transport_security_include_subdomains

        self.referrer_policy = referrer_policy

        self.session_cookie_secure = session_cookie_secure

        if session_cookie_http_only:
            app.config['SESSION_COOKIE_HTTPONLY'] = True

        self.force_file_save = force_file_save

        self.app = app

        app.after_request(self._set_response_headers)

    def _get_local_options(self):
        view_function = flask.current_app.view_functions.get(
            flask.request.endpoint)
        view_options = getattr(
            view_function, 'talisman_view_options', {})

        view_options.setdefault('frame_options', self.frame_options)
        view_options.setdefault(
            'frame_options_allow_from', self.frame_options_allow_from)
        view_options.setdefault(
            'feature_policy', self.feature_policy
        )

        return view_options

    def _set_response_headers(self, response):
        """Applies all configured headers to the given response."""
        options = self._get_local_options()
        self._set_feature_headers(response.headers, options)
        self._set_frame_options_headers(response.headers, options)
        self._set_hsts_headers(response.headers)
        self._set_referrer_policy_headers(response.headers)
        return response

    def _set_feature_headers(self, headers, options):
        if not options['feature_policy']:
            return

        headers['Feature-Policy'] = options['feature_policy']

    def _set_frame_options_headers(self, headers, options):
        if not options['frame_options']:
            return
        headers['X-Frame-Options'] = options['frame_options']

        if options['frame_options'] == ALLOW_FROM:
            headers['X-Frame-Options'] += " {}".format(options['frame_options_allow_from'])


    def _set_hsts_headers(self, headers):
        criteria = [
            flask.request.is_secure,
            flask.request.headers.get('X-Forwarded-Proto', 'http') == 'https',
        ]
        if not self.strict_transport_security or not any(criteria):
            return

        value = f'max-age={self.strict_transport_security_max_age}'

        if self.strict_transport_security_include_subdomains:
            value += '; includeSubDomains'

        if self.strict_transport_security_preload:
            value += '; preload'

        headers['Strict-Transport-Security'] = value

    def _set_referrer_policy_headers(self, headers):
        headers['Referrer-Policy'] = self.referrer_policy

    def __call__(self, **kwargs):
        """Use talisman as a decorator to configure options for a particular
        view.

        Only frame_options and frame_options_allow_from can be set on a per-view basis.

        Example:

            app = Flask(__name__)
            talisman = Talisman(app)

            @app.route('/normal')
            def normal():
                return 'Normal'

            @app.route('/embeddable')
            @talisman(frame_options=ALLOW_FROM, frame_options_allow_from='*')
            def embeddable():
                return 'Embeddable'
        """
        def decorator(f):
            setattr(f, 'talisman_view_options', kwargs)
            return f
        return decorator


try:
    import secrets
    get_random_string = secrets.token_urlsafe  # pragma: no cover

except ImportError:  # pragma: no cover
    import random
    import string
    rnd = random.SystemRandom()

    def get_random_string(length):
        allowed_chars = (
            string.ascii_lowercase +
            string.ascii_uppercase +
            string.digits
        )
        return ''.join(
            rnd.choice(allowed_chars)
            for _ in range(length)
        )
