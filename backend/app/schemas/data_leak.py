from typing import List, Literal

from pydantic import BaseModel, Field, PositiveInt
from schemas.breaches import Breach as BreachSchema
from schemas.breaches import BreachShow
from schemas.data_types import DataType as DataTypeSchema


class DataLeakInput(BaseModel):
    value: str
    # TODO: Traer de la bdd los nombres de las llaves
    dtype: Literal["email", "phone", "rut"]


class DataLeakBase(BaseModel):
    hash_value: str


class DataLeakCreate(DataLeakBase):
    pass


class DataLeak(DataLeakBase):
    id: PositiveInt
    data_type: DataTypeSchema
    breach_found: BreachSchema
    found_with: List[DataTypeSchema]

    class Config:
        orm_mode = True


class DataLeakShow(BaseModel):
    data_type: str = Field(validation_alias="data_type_display")
    breach_found: BreachShow
    found_with: List[str] = Field(validation_alias="found_with_display")
