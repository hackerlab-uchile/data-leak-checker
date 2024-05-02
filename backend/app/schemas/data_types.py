from typing import List

from pydantic import BaseModel, PositiveInt


class DataTypeBase(BaseModel):
    name: str


class DataTypeCreate(DataTypeBase):
    pass


class DataType(DataTypeBase):
    id: PositiveInt

    class Config:
        orm_model = True


class DataTypeShow(DataTypeBase):
    security_tips: List[str]

    class Config:
        orm_model = True
