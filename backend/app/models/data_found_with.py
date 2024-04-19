from core.database import Base
from models.data_type import ArrayOfEnum, DataType, DataTypePostgresEnum
from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column


class DataFoundWith(Base):
    __tablename__ = "data_found_with"
    data_leak_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_leak.id"), primary_key=True
    )
    data_type: Mapped[DataType] = mapped_column(
        ArrayOfEnum(DataTypePostgresEnum),
        primary_key=True,
        nullable=False,
    )

    def __repr__(self):
        return f"FoundWith(={self.data_leak_id}, data_type={self.data_type})"
