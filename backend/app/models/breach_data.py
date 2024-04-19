from core.database import Base
from models.data_type import DataType
from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column


class BreachData(Base):
    __tablename__ = "breach_data"
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breach.id"), primary_key=True
    )
    data_type: Mapped[str] = mapped_column(
        Enum(DataType), primary_key=True, nullable=False
    )

    def __repr__(self):
        return f"BreachData(breach_id={self.breach_id}, data_type={self.data_type})"
