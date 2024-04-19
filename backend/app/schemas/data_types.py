from pydantic import BaseModel, PositiveInt


class DataTypeBase(BaseModel):
    name: str


class DataTypeCreate(DataTypeBase):
    pass


class DataType(DataTypeBase):
    id: PositiveInt

    class Config:
        orm_model = True
