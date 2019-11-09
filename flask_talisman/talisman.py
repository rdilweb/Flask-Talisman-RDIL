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
from secrets import token_urlsafe

import flask

SAMEORIGIN = 'SAMEORIGIN'
ALLOW_FROM = 'ALLOW-FROM'

DEFAULT_REFERRER_POLICY = 'strict-origin-when-cross-origin'


class Talisman(object):
    """
    Talisman is a Flask extension for HTTP security headers.
    """

    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.app = app
            self.init_app(**kwargs)

    def init_app(
            self,
            feature_policy=None,
            force_https_permanent=False,
            force_file_save=False,
            frame_options=SAMEORIGIN,
            frame_options_allow_from=None,
            referrer_policy=DEFAULT_REFERRER_POLICY,
            session_cookie_secure=True,
            session_cookie_http_only=True
    ):
        """
        Initialization.

        Args:
            feature_policy: A string or dictionary describing the
                feature policy for the response.
            force_https_permanent: Uses 301 instead of 302 redirects.
            frame_options: Sets the X-Frame-Options header, defaults to
                SAMEORIGIN.
            frame_options_allow_from: Used when frame_options is set to
                ALLOW_FROM and is a string of domains to allow frame embedding.
            referrer_policy: A string describing the referrer policy for the
                response.
            session_cookie_secure: Forces the session cookie to only be sent
                over https. Disabled in debug mode.
            session_cookie_http_only: Prevents JavaScript from reading the
                session cookie.
            force_file_save: Prevents the user from opening a file download
                directly on >= IE 8
        """
        if feature_policy is None:
            feature_policy = {}
        if isinstance(feature_policy, dict):
            self.feature_policy = OrderedDict(feature_policy)
        else:
            self.feature_policy = feature_policy
        self.force_https_permanent = force_https_permanent

        self.frame_options = frame_options
        self.frame_options_allow_from = frame_options_allow_from

        self.referrer_policy = referrer_policy

        self.session_cookie_secure = session_cookie_secure

        if session_cookie_http_only:
            self.app.config['SESSION_COOKIE_HTTPONLY'] = True

        self.force_file_save = force_file_save

        self.app.after_request(self._set_response_headers)

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


get_random_string = token_urlsafe
