from typing import List, Optional

from core.database import Base
from models.data_type import ArrayOfEnum, DataType, DataTypePostgresEnum
from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class Breach(Base):
    __tablename__ = "breach"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(300))
    breach_date: Mapped[Date] = mapped_column(Date)
    confirmed: Mapped[bool] = mapped_column(Boolean)
    is_sensitive: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # data_breached: Mapped[List[DataType]] = relationship(secondary="breach_data")
    data_breached: Mapped[List[str]] = mapped_column(
        ArrayOfEnum(DataTypePostgresEnum), nullable=False
    )

    def __repr__(self):
        return f"Breach(id={self.id}, name={self.name}, description={self.description[:10]}[...], breach_date={self.breach_date}), data_breached={self.data_breached}"
