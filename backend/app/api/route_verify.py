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
