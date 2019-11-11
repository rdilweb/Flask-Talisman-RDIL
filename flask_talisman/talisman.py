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

DEFAULT_REFERRER_POLICY = 'strict-origin-when-cross-origin'


class Talisman:
    def __init__(
            self,
            app=None,
            force_https_permanent=False,
            force_file_save=False,
            referrer_policy=DEFAULT_REFERRER_POLICY,
            session_cookie_secure=True,
            session_cookie_http_only=True
    ):
        """
        Initialization.

        Args:
            force_https_permanent: Uses 301 instead of 302 redirects.
            referrer_policy: A string describing the referrer policy for the response.
            session_cookie_secure: Forces the session cookie to only be sent over https. Disabled in debug mode.
            session_cookie_http_only: Prevents JavaScript from reading the session cookie.
            force_file_save: Prevents the user from opening a file download directly on >= IE 8
        """
        if app is not None:
            self.app = app

        self.force_https_permanent = force_https_permanent

        self.referrer_policy = referrer_policy

        self.session_cookie_secure = session_cookie_secure

        if session_cookie_http_only:
            self.app.config['SESSION_COOKIE_HTTPONLY'] = True

        self.force_file_save = force_file_save

        self.app.after_request(self._set_response_headers)

    def _set_response_headers(self, response):
        """Applies all configured headers to the given response."""
        headers = response.headers

        headers['X-XSS-Protection'] = '1; mode=block'

        if self.force_file_save:
            headers['X-Download-Options'] = 'noopen'

        headers['Referrer-Policy'] = self.referrer_policy

        return response
