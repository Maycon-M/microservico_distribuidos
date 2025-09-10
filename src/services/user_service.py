from __future__ import annotations
from sqlalchemy.orm import Session

from src.domain.users import UserCreate
from src.interfaces.repositories.user_repo_interface import UserRepoInterface
from src.interfaces.services.user_service_interface import UserServiceInterface
from src.models.entities.user import User

class UserService(UserServiceInterface):
    def __init__(self, users: UserRepoInterface):
        self.__users = users

    def create(self, db: Session, params: UserCreate) -> User:
        existing = self.__users.get_by_email(db, params.email)
        if existing:
            raise ValueError("email_already_registered")
        return self.__users.create(db, params)

    def get_by_email(self, db: Session, email: str) -> User | None:
        return self.__users.get_by_email(db, email)

    def get(self, db: Session, user_id: int) -> User | None:
        return self.__users.get(db, user_id)

