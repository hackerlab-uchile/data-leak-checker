import re

from pydantic import AfterValidator
from typing_extensions import Annotated


def chilean_mobile_number_validator(v: str) -> str:
    assert isinstance(v, str), "Input must be a string"
    v_clean = v.strip()
    assert len(v_clean) <= 12, f"{v_clean[:13]}(...) is more than 12 characters long!"
    pattern = r"(((\+)?56)?9)?[\d]{8}"
    assert (
        re.fullmatch(pattern, v_clean) is not None
    ), f"{v_clean} has not the expected format for a chilean phone number. Examples: +56911223344, 56911223344, 911223344, 11223344"
    if len(v_clean) == 12:  # +56911223344
        return v_clean
    elif len(v_clean) == 11:  # 56911223344
        return "+" + v_clean
    elif len(v_clean) == 9:  # 911223344
        return "+56" + v_clean
    else:  # 11223344
        assert (
            len(v_clean) == 8
        ), f"{v_clean} of length {len(v_clean)} is not a valid chilean mobile number"
        return "+569" + v_clean


ChileanMobileNumber = Annotated[str, AfterValidator(chilean_mobile_number_validator)]
