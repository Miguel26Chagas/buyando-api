import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime

load_dotenv()

SECRET_KEYS = os.getenv('SECRET_KEYS')
ALG = os.getenv('ALG')

def crypt_password():
    pwd_context = CryptContext(
        schemes='argon2',
        deprecated="auto"
    )
    return pwd_context

def token(user_id, user_name, date:datetime):
    date = date
    claims = {
        'sub': user_id,
        'user': user_name,
        'date': int(date.timestamp())
    }

    token = jwt.encode(claims, SECRET_KEYS, ALG)
    return token