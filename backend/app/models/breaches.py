from core.database import Base
from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Breach(Base):
    __tablename__ = "breaches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(300))
    breach_date: Mapped[Date] = mapped_column(Date)
    confirmed: Mapped[bool] = mapped_column(Boolean)
    is_sensitive: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"Breach(id={self.id}, name={self.name}, description={self.description[:10]}[...], breach_date={self.breach_date})"
