from core.database import Base
from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.sql import func


class Breach(Base):
    __tablename__ = "breaches"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(300))
    breach_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())
    confirmed = Column(Boolean)
    is_sensitive = Column(Boolean)

    def __repr__(self):
        return f"Breach(id={self.id}, name={self.name}, description={self.description[:10]}[...], breach_date={self.breach_date})"
