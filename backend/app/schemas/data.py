from datetime import datetime

from pydantic import BaseModel, PositiveInt


class DataBase(BaseModel):
    value: str


class DataCreate(DataBase):
    type_id: int


class Breach(DataBase):
    id: PositiveInt
    created_at: datetime

    class Config:
        orm_model = True
