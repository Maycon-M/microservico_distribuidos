from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from src.domain.reminders import ReminderCreate
from src.interfaces.repositories.reminder_repo_interface import ReminderRepoInterface
from src.models.entities.reminder import Reminder

class ReminderRepo(ReminderRepoInterface):
    def create(self, db: Session, reminder_params: ReminderCreate) -> Reminder:
        try:
            new_reminder = Reminder(
                user_id=reminder_params.user_id,
                medicine_id=reminder_params.medicine_id,
                start_date=reminder_params.start_date,
                end_date=reminder_params.end_date,
                times_of_day=reminder_params.times_of_day,
                days_mask=reminder_params.days_mask,
                next_run_at=None,
                active=True,                                
            )
            
            db.add(new_reminder)
            db.flush()
            db.refresh(new_reminder)
            return new_reminder
        except Exception as e:
            db.rollback()
            raise e
    
    def get(self, db: Session, reminder_id: int): 
        return db.get(Reminder, reminder_id)
    
    def list_upcoming_24h(self, db: Session, user_id: int):
        now = datetime.now(timezone.utc)
        soon = now + timedelta(hours=24)
        stmt = select(Reminder).where(Reminder.user_id==user_id, Reminder.active==True, Reminder.next_run_at!=None, Reminder.next_run_at<=soon)
        return list(db.scalars(stmt))
