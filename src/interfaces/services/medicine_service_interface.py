from __future__ import annotations
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from src.domain.medicines import MedicineCreate
from src.models.entities.medicine import Medicine


class MedicineServiceInterface(ABC):

    @abstractmethod
    def create(self, db: Session, params: MedicineCreate) -> Medicine:
        raise NotImplementedError

    @abstractmethod
    def get(self, db: Session, med_id: int) -> Medicine | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, db: Session, user_id: int) -> list[Medicine]:
        raise NotImplementedError

