from typing import List

from core.database import Base
from models.breach import Breach
from models.data_type import ArrayOfEnum, DataType, DataTypePostgresEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils.types.choice import ChoiceType


class DataLeak(Base):
    __tablename__ = "data_leak"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, autoincrement=True
    )
    hash_value: Mapped[str] = mapped_column(
        String(64), primary_key=True, nullable=False
    )
    # data_type: Mapped[DataType] = mapped_column(
    #     ChoiceType(DataType), primary_key=True, nullable=False
    # )
    data_type: Mapped[str] = mapped_column(
        DataTypePostgresEnum,
        primary_key=True,
        nullable=False,
    )
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breach.id"), primary_key=True, nullable=False
    )

    found_with: Mapped[List[str]] = mapped_column(
        ArrayOfEnum(DataTypePostgresEnum),
        primary_key=True,
        nullable=False,
    )

    breach_found: Mapped["Breach"] = relationship("Breach", foreign_keys=[breach_id])
    # found_with: Mapped[List[DataType]] = relationship(secondary="data_found_with")

    def __repr__(self):
        return f"DataLeak(id={self.id}, hash_value={self.hash_value}, data_type={self.data_type}, breach_found={self.breach_found}, found_with={self.found_with})"
