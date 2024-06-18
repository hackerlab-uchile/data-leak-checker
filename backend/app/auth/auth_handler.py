from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from core.config import JWT_ALGORITHM, JWT_EXPIRE_MINUTES, JWT_SECRET
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyCookie
from schemas.token import TokenPayload

cookie_scheme = APIKeyCookie(
    name="token", description="Allows sensitive breaches search", auto_error=False
)


def create_jwt_token(
    value: str,
    dtype: str,
    expires_delta: timedelta = timedelta(minutes=JWT_EXPIRE_MINUTES),
) -> str:
    payload = {
        "value": value,
        "dtype": dtype,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def get_jwt_token(token: Optional[str] = Security(cookie_scheme)) -> TokenPayload:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token is None:
        print("NO TOKEN")
        raise credentials_exception
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        value = payload.get("value")
        dtype = payload.get("dtype")
        print(f"{value=}")
        print(f"{dtype=}")
        if value is None or dtype is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        print("Error token decode")
        raise credentials_exception
    return TokenPayload(value=value, dtype=dtype)
