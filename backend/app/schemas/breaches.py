from datetime import date, datetime
from typing import List

from pydantic import BaseModel, PositiveInt


class BreachBase(BaseModel):
    name: str
    description: str
    breach_date: date
    confirmed: bool
    is_sensitive: bool


class BreachCreate(BreachBase):
    pass


class Breach(BreachBase):
    id: PositiveInt
    created_at: datetime

    class Config:
        orm_mode = True


class BreachShow(BreachBase):
    created_at: datetime
    data_types: List[str]

    class Config:
        orm_mode = True
