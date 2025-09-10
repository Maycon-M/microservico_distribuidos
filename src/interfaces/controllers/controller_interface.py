from __future__ import annotations
from abc import ABC, abstractmethod
from src.domain.http.http_request import HttpRequest
from src.domain.http.http_response import HttpResponse


class ControllerInterface(ABC):
    @abstractmethod
    def handle(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError
