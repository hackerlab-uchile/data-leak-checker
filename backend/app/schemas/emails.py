from pydantic import BaseModel, PositiveInt
from schemas.breaches import Breach


class EmailBase(BaseModel):
    email: str
    breach_found : PositiveInt

class Email(EmailBase):
    id: PositiveInt
    breach: Breach
    
    class Config:
        orm_model = True