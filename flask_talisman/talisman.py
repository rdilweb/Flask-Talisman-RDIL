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
            force_file_save=False,
            referrer_policy=DEFAULT_REFERRER_POLICY,
            session_cookie_secure=True,
            session_cookie_http_only=True,
            content_type_nosniff=True,
            frame_options=None
    ):
        """
        Initialization.

        Args:
            referrer_policy: A string describing the referrer policy for the response.
            session_cookie_secure: Forces the session cookie to only be sent over https. Disabled in debug mode.
            session_cookie_http_only: Prevents JavaScript from reading the session cookie.
            force_file_save: Prevents the user from opening a file download directly on >= IE 8
            content_type_nosniff: Prevents the browser from trying to detect the response type (XSS fix).
            frame_options: Set the frame options header to fix clickjacking (can be None, or the string for the header).
        """
        if app is not None:
            self.app = app

        self.referrer_policy = referrer_policy

        self.session_cookie_secure = session_cookie_secure

        if session_cookie_http_only:
            self.app.config['SESSION_COOKIE_HTTPONLY'] = True

        self.force_file_save = force_file_save

        self.content_type_nosniff = content_type_nosniff

        self.frame_options = frame_options

        self.app.after_request(self._set_response_headers)

    def _set_response_headers(self, response):
        """Applies all configured headers to the given response."""

        response.headers['X-XSS-Protection'] = '1; mode=block'

        if self.force_file_save:
            response.headers['X-Download-Options'] = 'noopen'

        if self.referrer_policy is not None:
            response.headers['Referrer-Policy'] = self.referrer_policy

        if self.content_type_nosniff:
            response.headers['X-Content-Type-Options'] = 'nosniff'
        
        if self.frame_options in ["sameorigin", "deny"]:
            response.headers['X-Frame-Options'] = self.frame_options

        return response
