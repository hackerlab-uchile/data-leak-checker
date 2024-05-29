import os
import random
from datetime import datetime, timedelta, timezone

import requests
from auth.auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_jwt_token
from core.config import SMTP_PASSWORD, SMTP_SERVER, SMTP_USERNAME
from core.database import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from models.data_type import DataType
from pydantic import EmailStr
from repositories.verification_code_repository import (
    delete_verification_code,
    get_verification_code,
    get_verification_code_by_value_and_data_type,
    save_verification_code,
)
from schemas.verification_code import VerificationCodeCreate, VerificationCodeShow
from sqlalchemy.orm import Session

router = APIRouter()


def get_mail_conf() -> ConnectionConfig | None:
    if SMTP_PASSWORD and SMTP_USERNAME and SMTP_SERVER:
        return ConnectionConfig(
            MAIL_USERNAME=SMTP_USERNAME,
            MAIL_PASSWORD=SMTP_PASSWORD,
            MAIL_FROM=SMTP_USERNAME,
            MAIL_PORT=587,
            MAIL_SERVER=SMTP_SERVER,
            # MAIL_FROM_NAME="Verificación DataLeakChecker",
            MAIL_STARTTLS=True,
            # MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            # MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
    print(
        "Warning: Couldn't complete email configuration. USERNAME, PASSWORD or SERVER for SMTP server not found"
    )
    return None


def generate_random_code() -> int:
    return random.randrange(100_000, 1_000_000)


@router.post("/send/email/")
async def send_email_verify(email: EmailStr, db: Session = Depends(get_db)):
    random_code = generate_random_code()
    html = f"""<p>¡Hola! A continuación, puedes ver tu código de verificación. ¡No lo compartas!</p>
    <p><b>{random_code}</b></p>
    """

    message = MessageSchema(
        subject="Verificación de correo electrónico",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )
    conf = get_mail_conf()
    # TODO: Construir una dependecy que me entregue el email dtype
    dtype = db.query(DataType).filter(DataType.name == "email").first()
    if conf and dtype:
        fm = FastMail(conf)
        await fm.send_message(message)
        vcode = VerificationCodeCreate(
            code=random_code, associated_value=email, data_type_id=dtype.id
        )
        # If already exists, we delete it
        old_vcode = get_verification_code_by_value_and_data_type(db, email, dtype.id)
        if old_vcode:
            delete_verification_code(db, old_vcode)
        save_verification_code(db=db, vcode=vcode)

        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return JSONResponse(status_code=503, content={"message": "Servicio no disponible"})


@router.post("/code/email/")
async def verify_code_email(
    verification_code: VerificationCodeShow, db: Session = Depends(get_db)
):
    vcode = get_verification_code(verification_code, db)
    if vcode:
        token = create_jwt_token(
            value=vcode.associated_value, dtype=vcode.data_type.name
        )
        delete_verification_code(db, vcode)
        response = JSONResponse(
            status_code=200, content={"message": "Code verification successful"}
        )
        response.set_cookie(
            key="token",
            value=token,
            expires=datetime.now(timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            secure=True,
            httponly=True,
            samesite="strict",
        )
        return response
    return JSONResponse(
        status_code=404, content={"message": "Invalid verification code"}
    )


@router.post("/send/sms/")
async def send_sms_verify(phone: str):
    SERVICE_ID = os.getenv("TWILIO_SERVICE_SID", "")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    url = f"https://verify.twilio.com/v2/Services/{SERVICE_ID}/Verifications"
    data = {"To": "+56965672517", "Channel": "sms"}
    auth = (ACCOUNT_SID, AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    print("---> Status code:", response.status_code)
    return response.json()


@router.post("/phone/code/")
async def verify_phone_code(code: str):
    SERVICE_ID = os.getenv("TWILIO_SERVICE_SID", "")
    AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    url = f"https://verify.twilio.com/v2/Services/{SERVICE_ID}/VerificationCheck"
    data = {"To": "+56965672517", "Code": code}
    auth = (ACCOUNT_SID, AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    content = response.json()
    if response.status_code == 200:
        if content.get("valid"):
            print("Valid Code!")
        else:
            print("Code not valid :c")
    else:
        print("Oops, something went wrong!")
    return content
