from typing import List

from auth.auth_handler import get_jwt_token, validate_sensitive_search
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.breach import Breach
from models.data_leak import DataLeak
from models.data_type import DataType
from schemas.data_leak import DataLeakInput, DataLeakShow
from schemas.token import TokenPayload
from sqlalchemy import desc, false, true
from sqlalchemy.orm import Session
from utils.crytpography import get_hash

router = APIRouter()


@router.post("/data/", response_model=List[DataLeakShow])
def get_breaches_info(
    payload: DataLeakInput,
    is_full_search: bool = Depends(validate_sensitive_search),
    db: Session = Depends(get_db),
):
    """Returns information about data breaches related to a value and type

    If searched value and data type matches the information of a valid JWT token, then it includes
    sensitive breaches in its result.
    """
    hash_value = get_hash(payload.value)
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data type {payload.dtype}",
        )
    breaches_query = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == hash_value)
        .filter(DataLeak.data_type_id == dtype.id)
    )
    if not is_full_search:
        breaches_query = breaches_query.filter(Breach.is_sensitive == false())

    found_breaches = breaches_query.order_by(desc(Breach.breach_date)).all()
    return found_breaches


@router.post("/data/public/", response_model=List[DataLeakShow])
def get_breaches_public_info(payload: DataLeakInput, db: Session = Depends(get_db)):
    """Returns information about non sensitive data breaches related to a value and type"""
    hash_value = get_hash(payload.value)
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data type {payload.dtype}",
        )
    found_breaches = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == hash_value)
        .filter(DataLeak.data_type_id == dtype.id)
        .filter(Breach.is_sensitive == false())
        .order_by(desc(Breach.breach_date))
    ).all()
    return found_breaches


@router.get("/data/sensitive/", response_model=List[DataLeakShow])
def get_sensitive_breaches(
    payload: TokenPayload = Depends(get_jwt_token), db: Session = Depends(get_db)
):
    """Returns information about SENSITIVE data breaches related to a value and type"""
    hash_value = get_hash(payload.value)
    dtype = db.query(DataType).filter(DataType.name == payload.dtype).first()
    if dtype is None:
        # TODO: Throw error
        # TODO: Se puede hacer una dependency, que entregue el dtype correspondiente
        # TODO: Cómo se hacía una dependecy? xd
        return []
    found_breaches = (
        db.query(DataLeak)
        .join(Breach, Breach.id == DataLeak.breach_id)
        .filter(DataLeak.hash_value == hash_value)
        .filter(DataLeak.data_type_id == dtype.id)
        .filter(Breach.is_sensitive == true())
        .order_by(desc(Breach.breach_date))
    ).all()
    return found_breaches
