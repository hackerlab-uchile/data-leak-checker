from datetime import datetime, timedelta, timezone

import requests
from auth.auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_jwt_token
from core.config import (
    SMTP_PASSWORD,
    SMTP_SERVER,
    SMTP_USERNAME,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_SENDER_NUMBER,
)
from core.database import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from repositories.verification_code_repository import (
    delete_verification_code,
    generate_new_verification_code,
    get_verification_code,
)
from schemas.verification_code import VerificationCodeShow
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


@router.post("/send/email/")
async def send_email_verify(email: EmailStr, db: Session = Depends(get_db)):
    vcode = generate_new_verification_code(value=email, dtype_name="email", db=db)
    html = f"""<p>¡Hola! A continuación, puedes ver tu código de verificación. ¡No lo compartas!</p>
    <p><b>{vcode.code}</b></p>
    """
    message = MessageSchema(
        subject="Verificación de correo electrónico",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )
    conf = get_mail_conf()
    if conf:
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return JSONResponse(status_code=503, content={"message": "Servicio no disponible"})


@router.post("/send/sms/")
async def send_sms_verify(phone: str, db: Session = Depends(get_db)):
    # TODO: Verificar que es un número de teléfono válido (número chileno nomás?)
    vcode = generate_new_verification_code(value=phone, dtype_name="phone", db=db)
    msg = f"Su código de verificación: {vcode.code}. ¡No lo compartas!"
    url = (
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    )
    data = {"From": TWILIO_SENDER_NUMBER, "To": "+56965672517", "Body": msg}
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    if response.status_code == 201:
        return JSONResponse(status_code=200, content={"message": "Sms has been sent"})
    return JSONResponse(status_code=400, content={"message": "Sms was not sent"})


@router.post("/code/")
async def verify_code(
    verification_code: VerificationCodeShow, db: Session = Depends(get_db)
):
    vcode = get_verification_code(verification_code, db)
    if vcode:
        token = create_jwt_token(vcode.associated_value, vcode.data_type.name)
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
