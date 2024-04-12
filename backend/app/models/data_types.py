from core.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class DataType(Base):
    __tablename__ = "data_types"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dtype: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"DataType(id={self.id}, dtype={self.dtype})"
