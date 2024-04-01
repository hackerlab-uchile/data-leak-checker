from pydantic import BaseModel, PositiveInt


class EmailBase(BaseModel):
    value: str


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: PositiveInt

    class Config:
        orm_model = True
