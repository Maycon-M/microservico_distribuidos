from __future__ import annotations
from sqlalchemy.orm import Session

from src.domain.medicines import MedicineCreate
from src.interfaces.repositories.medicine_repo_interface import MedicineRepoInterface
from src.interfaces.repositories.user_repo_interface import UserRepoInterface
from src.interfaces.services.medicine_service_interface import MedicineServiceInterface
from src.models.entities.medicine import Medicine


class MedicineService(MedicineServiceInterface):
    def __init__(self, users: UserRepoInterface, meds: MedicineRepoInterface):
        self.__users = users
        self.__meds = meds

    def create(self, db: Session, params: MedicineCreate) -> Medicine:
        user = self.__users.get(db, params.user_id)
        if not user:
            raise ValueError("user_not_found")
        return self.__meds.create(db, params)

    def get(self, db: Session, med_id: int) -> Medicine | None:
        return self.__meds.get(db, med_id)

    def list_by_user(self, db: Session, user_id: int) -> list[Medicine]:
        return self.__meds.list_by_user(db, user_id)

