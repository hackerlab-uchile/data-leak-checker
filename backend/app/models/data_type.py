from core.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class DataType(Base):
    __tablename__ = "data_type"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"DataType(id={self.id}, name={self.name})"
