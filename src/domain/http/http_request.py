from __future__ import annotations
from typing import Any, Dict
from sqlalchemy.orm import Session


class HttpRequest:

    def __init__(
        self,
        body: Dict[str, Any] | Any | None = None,
        param: Dict[str, Any] | None = None,
        headers: Dict[str, Any] | None = None,
        token_infos: Dict[str, Any] | None = None,
        db: Session | None = None,
    ) -> None:
        self.body = body
        self.param = param or {}
        self.headers = headers or {}
        self.token_infos = token_infos or {}
        self.db = db

