from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, time
from sqlalchemy.orm import Session

class ReminderServiceInterface(ABC):

    @abstractmethod
    def create(self, db: Session, user_id: int, medicine_id: int, start_date: date, end_date: date | None, times_of_day: list[time], days_mask: int = 127):
        raise NotImplementedError

    @abstractmethod
    def recalc_next(self, db: Session, reminder_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def upcoming_24h(self, db: Session, user_id: int):
        raise NotImplementedError
