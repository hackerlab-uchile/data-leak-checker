from core.database import Base
from sqlalchemy import Column, Integer, String


class DataType(Base):
    __tablename__ = "data_types"
    id = Column(Integer, primary_key=True)
    dtype = Column(String(50))

    def __repr__(self):
        return f"DataType(id={self.id}, dtype={self.dtype})"