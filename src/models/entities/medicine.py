from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, BigInteger, Numeric, Text, ForeignKey, func

from src.models.settings.base import Base

class Medicine(Base):
    __tablename__ = "medicines"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    dose_amount: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    dose_unit: Mapped[str] = mapped_column(String(16), nullable=False, default="mg")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")

    def __repr__(self) -> str:
        return f"<Medicine(id={self.id}, name={self.name}, dose={self.dose_amount}{self.dose_unit})>"
