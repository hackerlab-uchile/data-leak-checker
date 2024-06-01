from datetime import datetime, timedelta, timezone

import requests
from auth.auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_jwt_token
from core.config import (
    DEV_RECEIVER_NUMBER,
    IN_PROD,
    SMTP_PASSWORD,
    SMTP_SERVER,
    SMTP_USERNAME,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_SENDER_NUMBER,
)
from core.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from repositories.data_type_repository import get_data_type_by_name
from repositories.user import get_user_or_create
from repositories.verification_code_repository import (
    generate_new_verification_code,
    get_verification_code,
    mark_verification_code_as_used,
)
from schemas.custom_fields import ChileanMobileNumber
from schemas.verification_code import VerificationCodeInput, VerificationCodeShow
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
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )
    print(
        "Warning: Couldn't complete email configuration. USERNAME, PASSWORD or SERVER for SMTP server not found"
    )
    return None


@router.post("/send/email/")
async def send_email_verify(email: EmailStr, db: Session = Depends(get_db)):
    email_dtype = get_data_type_by_name(name="email", db=db)
    if email_dtype is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user = get_user_or_create(value=email, data_type_id=email_dtype.id, db=db)
    vcode = generate_new_verification_code(user_id=user.id, db=db)
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
    return JSONResponse(status_code=503, content={"message": "Service unavailable"})


@router.post("/send/sms/")
async def send_sms_verify(phone: ChileanMobileNumber, db: Session = Depends(get_db)):
    phone_dtype = get_data_type_by_name(name="phone_dtype", db=db)
    if phone_dtype is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    user = get_user_or_create(value=phone, data_type_id=phone_dtype.id, db=db)
    vcode = generate_new_verification_code(user_id=user.id, db=db)
    msg = f"Su código de verificación: {vcode.code}. ¡No lo compartas!"
    url = (
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    )
    receiver_number = DEV_RECEIVER_NUMBER
    if IN_PROD.lower() == "true":
        receiver_number = phone
    data = {"From": TWILIO_SENDER_NUMBER, "To": receiver_number, "Body": msg}
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    response = requests.post(url, data=data, auth=auth)
    if response.status_code == 201:
        return JSONResponse(status_code=200, content={"message": "Sms has been sent"})
    return JSONResponse(status_code=400, content={"message": "Sms was not sent"})


@router.post("/code/")
async def verify_code(
    verification_code: VerificationCodeInput, db: Session = Depends(get_db)
):
    vcode = get_verification_code(verification_code, db)
    if vcode is None:
        return JSONResponse(
            status_code=404, content={"message": "Invalid verification code"}
        )
    token = create_jwt_token(vcode.associated_value, vcode.value_type)
    mark_verification_code_as_used(vcode=vcode, db=db)
    response = JSONResponse(
        status_code=200, content={"message": "Code verification successful"}
    )
    response.set_cookie(
        key="token",
        value=token,
        expires=datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        secure=True,  # Put on false, for development purposes
        httponly=True,
        samesite="strict",
    )
    return response
