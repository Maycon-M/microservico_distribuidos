from __future__ import annotations
from datetime import date, time
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.domain.http.http_request import HttpRequest
from src.domain.http.http_response import HttpResponse
from src.interfaces.controllers.controller_interface import ControllerInterface
from src.services.reminder_service import ReminderService
from src.domain.reminders import ReminderCreate


class CreateReminderController(ControllerInterface):
    def __init__(self, svc: ReminderService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        body: ReminderCreate = request.body  # type: ignore
        try:
            r = self.__svc.create(
                db,
                user_id=body.user_id,
                medicine_id=body.medicine_id,
                start_date=body.start_date,
                end_date=body.end_date,
                times_of_day=body.times_of_day,
                days_mask=body.days_mask,
            )
            self.__svc.recalc_next(db, r.id)
            db.refresh(r)
            return HttpResponse(status_code=201, body=r)
        except ValueError as e:
            return HttpResponse(status_code=400, body={"error": str(e)})


class RecalcReminderController(ControllerInterface):
    def __init__(self, svc: ReminderService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        reminder_id = int(request.param.get("reminder_id"))  # type: ignore
        ok = self.__svc.recalc_next(db, reminder_id)
        if not ok:
            return HttpResponse(status_code=404, body={"error": "reminder_not_found"})
        return HttpResponse(status_code=200, body=True)


class Upcoming24hController(ControllerInterface):
    def __init__(self, svc: ReminderService):
        self.__svc = svc

    def handle(self, request: HttpRequest) -> HttpResponse:
        db = request.db  # type: ignore
        user_id = int(request.param.get("user_id"))  # type: ignore
        items = self.__svc.upcoming_24h(db, user_id)
        return HttpResponse(status_code=200, body=items)
