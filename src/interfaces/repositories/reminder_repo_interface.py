from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.domain.reminders import ReminderCreate
from src.models.entities.reminder import Reminder

class ReminderRepoInterface(ABC):
    
    @abstractmethod
    def create(self, db: Session, reminder_params: ReminderCreate) -> Reminder:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, db: Session, reminder_id: int): 
        raise NotImplementedError
    
    @abstractmethod
    def list_upcoming_24h(self, db: Session, user_id: int):
        raise NotImplementedError
