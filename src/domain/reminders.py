from datetime import date, time, datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator

def _validate_times(v: list[time]):
    if not v or len(v) == 0:
        raise ValueError("times_of_day_required")
    if len(v) > 8:
        raise ValueError("too_many_times")
    return v

class ReminderCreate(BaseModel):
    user_id: int
    medicine_id: int
    start_date: date
    end_date: date | None = None
    times_of_day: list[time] = Field(default_factory=list)
    days_mask: int = 127
    @field_validator("times_of_day")
    @classmethod
    def _v_times(cls, v): return _validate_times(v)

class ReminderOut(BaseModel):
    id: int
    user_id: int
    medicine_id: int
    start_date: date
    end_date: date | None
    times_of_day: list[time]
    days_mask: int
    next_run_at: datetime | None
    active: bool
    model_config = ConfigDict(from_attributes=True)
