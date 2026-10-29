import json
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

file_path = Path(__file__).resolve().parents[1] / "data" / "product.json"
users_file_path = Path(__file__).resolve().parents[1] / "data" / "users.json"

def get_all_products():
    with file_path.open("r", encoding="utf-8") as p:
        return json.load(p)

def create_all_products(products):
    with open(file_path,'w') as p:
         json.dump(products,p)

def get_all_users():
    with users_file_path.open("r", encoding="utf-8") as u:
        return json.load(u)
    
email_conf = ConnectionConfig(
    MAIL_USERNAME = "darshangowda1658@gmail.com",
    MAIL_PASSWORD = "***********",
    MAIL_FROM = "darshangowda1658@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Fast API",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def simple_send(email: str) :
    html = """<p>Hi, You're order placed successfully</p> """

    message = MessageSchema(
        subject="Order confirmation",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(email_conf)
    await fm.send_message(message)
    print("Email sent successfully")
    