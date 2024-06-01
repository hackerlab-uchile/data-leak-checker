from models.verification_code import CODE_LENGTH
from pydantic import BaseModel, Field, PositiveInt


class VerificationCodeBase(BaseModel):
    code: str = Field(max_length=CODE_LENGTH)


class VerificationCodeCreate(VerificationCodeBase):
    user_id: PositiveInt


class VerificationCodeInput(VerificationCodeBase):
    value: str
    dtype: str


class VerificationCodeShow(VerificationCodeBase):
    value: str = Field(validation_alias="associated_value")
    dtype: str = Field(validation_alias="value_type")
