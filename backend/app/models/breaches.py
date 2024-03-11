from core.database import Base
from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.sql import func


class Breach(Base):
    __tablename__ = "breaches"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    description = Column(String(300))
    breach_date = Column(Date)
    created_at = Column(Date, server_default=func.now())
    confirmed = Column(Boolean)
    is_sensitive = Column(Boolean)