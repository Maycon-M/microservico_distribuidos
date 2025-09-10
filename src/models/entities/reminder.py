from datetime import datetime, time, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Boolean, Date, DateTime, Time, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY

from src.models.settings.base import Base

class Reminder(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    medicine_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("medicines.id", ondelete="CASCADE"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    times_of_day: Mapped[list[time]] = mapped_column(ARRAY(Time), nullable=False)
    days_mask: Mapped[int] = mapped_column(nullable=False, default=127)
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")
    medicine = relationship("Medicine")
    
    def __repr__(self) -> str:
        return f"<Reminder(id={self.id}, user_id={self.user_id}, medicine_id={self.medicine_id}, active={self.active})>"
