from core.database import Base
from models.data_type import DataType
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class VerificationCode(Base):
    __tablename__ = "verification_code"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[int] = mapped_column(Integer, nullable=False)
    associated_value: Mapped[str] = mapped_column(String, nullable=False)
    data_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("data_type.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    data_type: Mapped["DataType"] = relationship(
        "DataType", foreign_keys=[data_type_id]
    )

    def __repr__(self):
        return f"VerificationCode(id={self.id}, code={self.code}, associated_value={self.associated_value} data_type_id={self.data_type_id})"
