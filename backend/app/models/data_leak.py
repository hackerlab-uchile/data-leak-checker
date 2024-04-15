from typing import List

from core.database import Base
from models.breach import Breach
from models.data_found_with import DataFoundWith
from models.data_type import DataType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DataLeak(Base):
    __tablename__ = "data_leak"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, autoincrement=True
    )
    hash_value: Mapped[str] = mapped_column(
        String(64), primary_key=True, nullable=False
    )
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), primary_key=True, nullable=False
    )
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breach.id"), primary_key=True, nullable=False
    )

    data_type: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[data_type_id]
    )
    breach_found: Mapped["Breach"] = relationship("Breach", foreign_keys=[breach_id])
    found_with: Mapped[List["DataType"]] = relationship(secondary="data_found_with")

    def __repr__(self):
        return f"DataLeak(id={self.id}, hash_value={self.hash_value}, data_type={self.data_type}, breach_found={self.breach_found}, found_with={self.found_with})"
