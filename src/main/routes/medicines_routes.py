from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from src.domain.medicines import MedicineCreate, MedicineOut
from src.main.composers.medicines_composer import (
    make_create_medicine_controller,
    make_get_medicine_controller,
    make_list_medicines_by_user_controller,
)
from src.models.settings.db_conn_handler import get_session
from src.domain.http.http_request import HttpRequest


router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post("", response_model=MedicineOut, status_code=201)
def create_medicine(payload: MedicineCreate, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_create_medicine_controller()
    http_req = HttpRequest(body=payload, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.get("/{med_id}", response_model=MedicineOut)
def get_medicine(med_id: int, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_get_medicine_controller()
    http_req = HttpRequest(param={"med_id": med_id}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.get("/by-user/{user_id}", response_model=list[MedicineOut])
def list_by_user(user_id: int, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_list_medicines_by_user_controller()
    http_req = HttpRequest(param={"user_id": user_id}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body
