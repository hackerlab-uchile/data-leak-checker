import os

import requests
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="DataLeakChecker",
    MAIL_PASSWORD="**********",
    MAIL_FROM="verify@dataleak.cl",
    MAIL_PORT=587,
    MAIL_SERVER="mail server",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


@router.post("/email/")
async def send_email_verify(email: EmailStr):
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


@router.post("/phone/")
async def send_phone_verify(phone: str):
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
