from __future__ import annotations

from src.domain.http.http_request import HttpRequest
from src.domain.http.http_response import HttpResponse
from src.domain.users import UserCreate
from src.interfaces.controllers.controller_interface import ControllerInterface
from src.services.user_service import UserService


class CreateUserController(ControllerInterface):
    def __init__(self, svc: UserService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        payload: UserCreate = request.body  # type: ignore
        try:
            created = self.__svc.create(db, payload)
            return HttpResponse(status_code=201, body=created)
        except ValueError as e:
            return HttpResponse(status_code=400, body={"error": str(e)})


class GetUserController(ControllerInterface):
    def __init__(self, svc: UserService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        user_id = int(request.param.get("user_id"))  # type: ignore
        user = self.__svc.get(db, user_id)
        if not user:
            return HttpResponse(status_code=404, body={"error": "user_not_found"})
        return HttpResponse(status_code=200, body=user)


class GetUserByEmailController(ControllerInterface):
    def __init__(self, svc: UserService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        email = str(request.param.get("email"))  # type: ignore
        user = self.__svc.get_by_email(db, email)
        if not user:
            return HttpResponse(status_code=404, body={"error": "user_not_found"})
        return HttpResponse(status_code=200, body=user)
