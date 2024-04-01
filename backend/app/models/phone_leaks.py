from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class PhoneLeak(Base):
    __tablename__ = "phone_leaks"
    breach_id = Column(Integer, ForeignKey("breaches.id"), primary_key=True)
    phone_id = Column(Integer, ForeignKey("phones.id"), primary_key=True)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    breach_found = relationship("Breach", foreign_keys=[breach_id])
    phone = relationship("Phone", foreign_keys=[phone_id])
    found_with = relationship("DataType", foreign_keys=[data_type_id])

    def __repr__(self):
        return f"PhoneLeak(breach_id={self.breach_id}, phone_id={self.phone_id}, created_at={self.created_at})"
