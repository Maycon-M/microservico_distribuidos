from __future__ import annotations
from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.domain.reminders import ReminderOut
from src.main.composers.reminders_composer import (
    make_create_reminder_controller,
    make_recalc_reminder_controller,
    make_upcoming_24h_controller,
)
from src.models.settings.db_conn_handler import get_session
from src.domain.http.http_request import HttpRequest


class ReminderCreateIn(BaseModel):
    user_id: int
    medicine_id: int
    start_date: date
    end_date: date | None = None
    times_of_day: list[time] = Field(default_factory=list)
    days_mask: int = 127


router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("", response_model=ReminderOut, status_code=201)
def create_reminder(payload: ReminderCreateIn, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_create_reminder_controller()
    http_req = HttpRequest(body=payload, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.post("/{reminder_id}/recalc", response_model=bool)
def recalc_next(reminder_id: int, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_recalc_reminder_controller()
    http_req = HttpRequest(param={"reminder_id": reminder_id}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.get("/upcoming/{user_id}", response_model=list[ReminderOut])
def upcoming_24h(user_id: int, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_upcoming_24h_controller()
    http_req = HttpRequest(param={"user_id": user_id}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body
