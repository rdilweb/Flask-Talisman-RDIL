import flask
from typing import Union


DEFAULT_REFERRER_POLICY: str


class Talisman:
    def __init__(
        self,
        app: flask.Flask = None,
        force_file_save: bool = False,
        referrer_policy: str = "strict-origin-when-cross-origin",
        session_cookie_secure: bool = True,
        session_cookie_http_only: bool = True,
        content_type_nosniff: bool = True,
        frame_options: Union[str, None] = None
    ): ...
