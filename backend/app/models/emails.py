
from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    breach_found = Column(Integer, ForeignKey("breaches.id"))
    breach = relationship("Breach", foreign_keys=[breach_found])