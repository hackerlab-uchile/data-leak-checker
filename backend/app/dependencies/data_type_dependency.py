from core.database import get_db
from fastapi import Depends, HTTPException, status
from repositories.data_type_repository import get_data_type_by_name
from sqlalchemy.orm import Session


def get_data_type_from_body(dtype: str, db: Session = Depends(get_db)):
    data_type = get_data_type_by_name(name=dtype, db=db)
    if data_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Type {dtype} not found"
        )
    return data_type
