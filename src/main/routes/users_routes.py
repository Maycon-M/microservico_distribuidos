from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from src.domain.users import UserCreate, UserOut
from src.main.composers.users_composer import (
    make_create_user_controller,
    make_get_user_controller,
    make_get_user_by_email_controller,
)
from src.models.settings.db_conn_handler import get_session
from src.domain.http.http_request import HttpRequest


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_create_user_controller()
    http_req = HttpRequest(body=payload, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_get_user_controller()
    http_req = HttpRequest(param={"user_id": user_id}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body


@router.get("/by-email", response_model=UserOut)
def get_user_by_email(email: str, response: Response, request: Request, db: Session = Depends(get_session)):
    controller = make_get_user_by_email_controller()
    http_req = HttpRequest(param={"email": email}, headers=dict(request.headers), db=db)
    http_res = controller.handle(http_req)
    if http_res.status_code >= 400:
        raise HTTPException(status_code=http_res.status_code, detail=http_res.body)
    response.status_code = http_res.status_code
    return http_res.body
