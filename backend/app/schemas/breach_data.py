from datetime import datetime

from pydantic import BaseModel, PositiveInt
from sqlalchemy import Integer


class BreachDataBase(BaseModel):
    breach_id: PositiveInt
    data_type_id: PositiveInt


class BreachDataCreate(BreachDataBase):
    pass


class BreachData(BreachDataBase):
    created_at: datetime

    class Config:
        orm_model = True
