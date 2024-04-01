from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class BreachData(Base):
    __tablename__ = "breach_data"
    breach_id = Column(Integer, ForeignKey("breaches.id"), primary_key=True)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    breach_found = relationship("Breach", foreign_keys=[breach_id])
    found_with = relationship("DataType", foreign_keys=[data_type_id])

    def __repr__(self):
        return f"BreachData(breach_id={self.breach_id}, data_type_id={self.data_type_id}, created_at={self.created_at})"
