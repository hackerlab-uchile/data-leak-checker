import os
import random

import requests
from core.config import SMTP_PASSWORD, SMTP_SERVER, SMTP_USERNAME
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

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
    return random.randrange(1_000, 10_000)


@router.post("/send/email/")
async def send_email_verify(email: EmailStr):
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
    if conf:
        fm = FastMail(conf)
        await fm.send_message(message)
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    return JSONResponse(status_code=503, content={"message": "Servicio no disponible"})


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
