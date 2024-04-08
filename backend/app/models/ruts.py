from core.database import Base
from sqlalchemy import CHAR, Column, Integer


class Rut(Base):
    __tablename__ = "ruts"
    id = Column(Integer, primary_key=True)
    value = Column(CHAR(64))

    def __repr__(self):
        return f"Rut(id={self.id}, rut={self.value})"
