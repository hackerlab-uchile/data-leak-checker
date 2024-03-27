from pydantic import BaseModel, PositiveInt


class PhoneBase(BaseModel):
    value: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: PositiveInt

    class Config:
        orm_model = True
