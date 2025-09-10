from __future__ import annotations
from sqlalchemy.orm import Session

from src.domain.http.http_request import HttpRequest
from src.domain.http.http_response import HttpResponse
from src.domain.medicines import MedicineCreate
from src.interfaces.controllers.controller_interface import ControllerInterface
from src.services.medicine_service import MedicineService


class CreateMedicineController(ControllerInterface):
    def __init__(self, svc: MedicineService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        body: MedicineCreate = request.body  # type: ignore
        try:
            created = self.__svc.create(db, body)
            return HttpResponse(status_code=201, body=created)
        except ValueError as e:
            return HttpResponse(status_code=400, body={"error": str(e)})


class GetMedicineController(ControllerInterface):
    def __init__(self, svc: MedicineService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        med_id = int(request.param.get("med_id"))  # type: ignore
        med = self.__svc.get(db, med_id)
        if not med:
            return HttpResponse(status_code=404, body={"error": "medicine_not_found"})
        return HttpResponse(status_code=200, body=med)


class ListMedicinesByUserController(ControllerInterface):
    def __init__(self, svc: MedicineService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        user_id = int(request.param.get("user_id"))  # type: ignore
        meds = self.__svc.list_by_user(db, user_id)
        return HttpResponse(status_code=200, body=meds)
