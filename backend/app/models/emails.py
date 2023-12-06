
from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    breach_found = Column(Integer, ForeignKey("breaches.id"))
    breach = relationship("Breach", foreign_keys=[breach_found])

    def __repr__(self):
        return f"Email(id={self.id}, email={self.email}, breach_found={self.breach_found}, breach={self.breach})"