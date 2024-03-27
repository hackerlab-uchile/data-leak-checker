from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class RutLeak(Base):
    __tablename__ = "rut_leaks"
    breach_id = Column(Integer, ForeignKey("breaches.id"), primary_key=True)
    rut_id = Column(Integer, ForeignKey("ruts.id"), primary_key=True)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    breach_found = relationship("Breach", foreign_keys=[breach_id])
    rut = relationship("Rut", foreign_keys=[rut_id])
    found_with = relationship("DataType", foreign_keys=[data_type_id])

    def __repr__(self):
        return f"RutLeak(breach_id={self.breach_id}, rut_id={self.rut_id}, created_at={self.created_at})"
