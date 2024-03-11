from core.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class DataLeak(Base):
    __tablename__ = "data_leaks"
    id = Column(Integer, primary_key=True)
    data_id = Column(Integer, ForeignKey("data.id"))
    breach_id = Column(Integer, ForeignKey("breaches.id"))
    data = relationship("Data", foreign_keys=[data_id])
    breach = relationship("Breach", foreign_keys=[breach_id])
    associated_data = Column(String(200))

    def __repr__(self):
        return f"DataLeak(id={self.id}, data={self.data}, breach={self.breach}, associated_data={self.associated_data})"