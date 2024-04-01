from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class EmailLeak(Base):
    __tablename__ = "email_leaks"
    breach_id = Column(Integer, ForeignKey("breaches.id"), primary_key=True)
    email_id = Column(Integer, ForeignKey("emails.id"), primary_key=True)
    data_type_id = Column(Integer, ForeignKey("data_types.id"), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    breach_found = relationship("Breach", foreign_keys=[breach_id])
    email = relationship("Email", foreign_keys=[email_id])
    found_with = relationship("DataType", foreign_keys=[data_type_id])

    def __repr__(self):
        return f"EmailLeak(breach_id={self.breach_id}, email_id={self.email_id}, created_at={self.created_at})"
