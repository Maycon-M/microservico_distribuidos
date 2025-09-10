from __future__ import annotations

from src.controllers.medicines_controller import (
    CreateMedicineController,
    GetMedicineController,
    ListMedicinesByUserController,
)
from src.models.repositories.user_repo import UserRepo
from src.models.repositories.medicine_repo import MedicineRepo
from src.services.medicine_service import MedicineService


def make_medicine_service() -> MedicineService:
    users_repo = UserRepo()
    meds_repo = MedicineRepo()
    return MedicineService(users_repo, meds_repo)


def make_create_medicine_controller() -> CreateMedicineController:
    return CreateMedicineController(make_medicine_service())


def make_get_medicine_controller() -> GetMedicineController:
    return GetMedicineController(make_medicine_service())


def make_list_medicines_by_user_controller() -> ListMedicinesByUserController:
    return ListMedicinesByUserController(make_medicine_service())

