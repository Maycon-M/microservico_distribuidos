from __future__ import annotations

from src.controllers.reminders_controller import (
    CreateReminderController,
    RecalcReminderController,
    Upcoming24hController,
)
from src.models.repositories.user_repo import UserRepo
from src.models.repositories.medicine_repo import MedicineRepo
from src.models.repositories.reminder_repo import ReminderRepo
from src.services.reminder_service import ReminderService


def make_reminder_service() -> ReminderService:
    users_repo = UserRepo()
    meds_repo = MedicineRepo()
    rems_repo = ReminderRepo()
    return ReminderService(users_repo, meds_repo, rems_repo)


def make_create_reminder_controller() -> CreateReminderController:
    return CreateReminderController(make_reminder_service())


def make_recalc_reminder_controller() -> RecalcReminderController:
    return RecalcReminderController(make_reminder_service())


def make_upcoming_24h_controller() -> Upcoming24hController:
    return Upcoming24hController(make_reminder_service())

