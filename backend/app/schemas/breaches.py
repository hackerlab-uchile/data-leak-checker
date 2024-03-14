
from datetime import datetime

from pydantic import BaseModel, PositiveInt


class BreachBase(BaseModel):
    name: str
    description: str
    breach_date: datetime
    confirmed: bool
    is_sensitive: bool

class BreachCreate(BreachBase):
    pass

class Breach(BreachBase):
    id: PositiveInt
    created_at: datetime
    
    class Config:
        orm_model = True