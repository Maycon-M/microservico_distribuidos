from __future__ import annotations
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from src.domain.users import UserCreate
from src.models.entities.user import User


class UserServiceInterface(ABC):

    @abstractmethod
    def create(self, db: Session, params: UserCreate) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get(self, db: Session, user_id: int) -> User | None:
        raise NotImplementedError

