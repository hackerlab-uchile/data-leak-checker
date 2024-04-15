from pydantic import BaseModel, PositiveInt
from schemas.breaches import Breach as BreachSchema
from schemas.data_types import DataType as DataTypeSchema


class DataLeakBase(BaseModel):
    hash_value: str


class DataLeakCreate(DataLeakBase):
    pass


class DataLeak(DataLeakBase):
    id: PositiveInt
    data_type: DataTypeSchema
    breach_found: BreachSchema
    found_with: DataTypeSchema

    class Config:
        orm_model = True
