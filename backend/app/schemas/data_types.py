from pydantic import BaseModel, PositiveInt


class DataTypeBase(BaseModel):
    dtype: str


class DataTypeCreate(DataTypeBase):
    pass


class DataType(DataTypeBase):
    id: PositiveInt

    class Config:
        orm_model = True
