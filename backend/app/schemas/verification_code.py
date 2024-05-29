from typing import Literal

from pydantic import BaseModel, PositiveInt


class VerificationCodeBase(BaseModel):
    code: PositiveInt


class VerificationCodeCreate(VerificationCodeBase):
    associated_value: str
    data_type_id: int


class VerificationCodeShow(VerificationCodeBase):
    associated_value: str
    dtype: Literal["email", "phone"]
