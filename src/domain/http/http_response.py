from __future__ import annotations
from typing import Any, Dict


class HttpResponse:

    def __init__(self, status_code: int, body: Dict[str, Any] | Any | None = None) -> None:
        self.status_code = status_code
        self.body = body

