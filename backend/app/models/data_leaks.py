from core.database import Base
from models.breaches import Breach
from models.data_types import DataType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DataLeak(Base):
    __tablename__ = "data_leaks"
    hash_value: Mapped[str] = mapped_column(
        String(64), primary_key=True, nullable=False
    )
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_types.id"), primary_key=True, nullable=False
    )
    breach_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("breaches.id"), primary_key=True, nullable=False
    )
    found_with_data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_types.id"), primary_key=True, nullable=True
    )

    data_type: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[data_type_id]
    )
    breach_found: Mapped["Breach"] = relationship("Breach", foreign_keys=[breach_id])
    found_with: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[found_with_data_type_id]
    )

    def __repr__(self):
        return f"DataLeak(hash_value={self.hash_value}, data_type={self.data_type}, breach_found={self.breach_found}, found_with={self.found_with})"
