from core.database import Base
from sqlalchemy import Column, Integer, String


class Rut(Base):
    __tablename__ = "ruts"
    id = Column(Integer, primary_key=True)
    value = Column(String(100))

    def __repr__(self):
        return f"Rut(id={self.id}, rut={self.value})"
