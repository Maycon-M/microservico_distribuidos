from __future__ import annotations

from src.controllers.users_controller import (
    CreateUserController,
    GetUserController,
    GetUserByEmailController,
)
from src.models.repositories.user_repo import UserRepo
from src.services.user_service import UserService


def make_user_service() -> UserService:
    users_repo = UserRepo()
    return UserService(users_repo)


def make_create_user_controller() -> CreateUserController:
    return CreateUserController(make_user_service())


def make_get_user_controller() -> GetUserController:
    return GetUserController(make_user_service())


def make_get_user_by_email_controller() -> GetUserByEmailController:
    return GetUserByEmailController(make_user_service())

