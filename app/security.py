import jwt
import os
from dotenv import load_dotenv

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login-form')
oaut2_form = OAuth2PasswordRequestForm


load_dotenv()

SECRET_KEYS = os.getenv('SECRET_KEYS')
ALG = os.getenv('ALG')

SCOPE_ROLE = {
    'admin': [],
    'seller': [],
    'buyer': []
}

def create_token(user: str, time):
    payload = {
        'sub': str(user.id),
        'scopes': SCOPE_ROLE[user.role],
        'exp': time
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEYS, ALG)
    return encoded_jwt

argon2_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto'
)

def hash_password(password):
    return argon2_context.hash(password)

def verify_password(password, hashed):
   return argon2_context.verify(password, hashed)