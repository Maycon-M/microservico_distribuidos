from __future__ import annotations
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session

from src.interfaces.services.reminder_service_interface import ReminderServiceInterface
from src.interfaces.repositories.medicine_repo_interface import MedicineRepoInterface
from src.interfaces.repositories.user_repo_interface import UserRepoInterface
from src.interfaces.repositories.reminder_repo_interface import ReminderRepoInterface
from src.domain.reminders import ReminderCreate

class ReminderService (ReminderServiceInterface):
    def __init__(self, users: UserRepoInterface, meds: MedicineRepoInterface, rems: ReminderRepoInterface):
        self.__users = users
        self.__meds = meds
        self.__rems = rems

    def __mask_matches(self, d: date, mask: int) -> bool:
        py = d.weekday()
        bit = {0:2,1:4,2:8,3:16,4:32,5:64,6:1}[py]
        return (mask & bit) != 0

    def __compute_next_run(self, tz: str, start_date: date, end_date: date | None, times: list[time], mask: int) -> datetime | None:
        tzinfo = ZoneInfo(tz)
        today_local = datetime.now(tzinfo).date()
        day = max(today_local, start_date)
        if end_date and day > end_date:
            return None

        for _ in range(0, 60):
            if self.__mask_matches(day, mask):
                now_local = datetime.now(tzinfo)
                for t in sorted(times):
                    candidate_local = datetime.combine(day, t, tzinfo)
                    if candidate_local >= now_local:
                        return candidate_local.astimezone(ZoneInfo("UTC"))
            day = day + timedelta(days=1)
            if end_date and day > end_date:
                break
        return None

    def create(self, db: Session, user_id: int, medicine_id: int, start_date: date, end_date: date | None, times_of_day: list[time], days_mask: int = 127):
        user = self.__users.get(db, user_id)
        if not user: raise ValueError("user_not_found")
        med = self.__meds.get(db, medicine_id)
        if not med or med.user_id != user_id: raise ValueError("medicine_not_found_or_mismatch")

        next_run = self.__compute_next_run(user.timezone, start_date, end_date, times_of_day, days_mask)
        entity = ReminderCreate(
            user_id=user_id,
            medicine_id=medicine_id,
            start_date=start_date,
            end_date=end_date,
            times_of_day=times_of_day,
            days_mask=days_mask,
            next_run_at=next_run,
        )
        return self.__rems.create(db, entity)

    def recalc_next(self, db: Session, reminder_id: int) -> bool:
        r = self.__rems.get(db, reminder_id)
        if not r: return False
        user_tz = r.user.timezone if r.user else "UTC"
        r.next_run_at = self.__compute_next_run(user_tz, r.start_date, r.end_date, r.times_of_day, r.days_mask)
        db.flush(); return True

    def upcoming_24h(self, db: Session, user_id: int):
        return self.__rems.list_upcoming_24h(db, user_id)
