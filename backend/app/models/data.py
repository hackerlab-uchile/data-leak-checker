from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    value = Column(String(100))
    type_id = Column(Integer, ForeignKey("data_types.id"))
    dtype = relationship("DataType", foreign_keys=[type_id])
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"Data(id={self.id}, value={self.value}, dtype={self.dtype}, created_at={self.created_at})"