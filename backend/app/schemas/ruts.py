from pydantic import BaseModel, PositiveInt


class RutBase(BaseModel):
    value: str


class RutCreate(RutBase):
    pass


class Rut(RutBase):
    id: PositiveInt

    class Config:
        orm_model = True
