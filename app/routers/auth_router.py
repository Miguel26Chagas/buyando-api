from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models import User
from app.schemas import UserSchema, LoginSchema
from app.security import crypt_password, token
from datetime import datetime, timedelta, timezone

import os
from dotenv import load_dotenv
load_dotenv()

EXP_MINUTE = float(os.getenv('EXP_MINUTE'))

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/')
async def create_user(data: UserSchema, db: Session = Depends(get_db)):
    query_user = db.query(User).filter(or_(User.name == data.name, User.email == data.email)).first()

    if query_user:
        raise HTTPException(
            status_code=401,
            detail='Nome ou email ja existente!'
        )
    
    password = crypt_password().hash(data.password)

    user = User(
        name=data.name,
        email=data.email,
        number_phone=data.number_phone,
        password=password,
        active=data.active,
        admin=data.admin,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail='Erro ao tentar criar Usuario'
        )
    
    return {'msg': f'Usuario {data.name} registado com sucesso'}

@router.post('/login')
async def login(data: LoginSchema, db: Session=Depends(get_db)):
    query_user = db.query(User).filter(User.email == data.email).first()

    password = crypt_password().verify(data.password, query_user.password)

    if not query_user or not password:
        raise HTTPException(
            status_code=401,
            detail='Email ou senha incorreta'
        )
    
    token_date = {
        'exp_date': datetime.now(timezone.utc) + timedelta(days=7),
        'access_date': datetime.now(timezone.utc) + timedelta(minutes=EXP_MINUTE),
    }
    
    access_token = token(query_user.id, query_user.name, token_date['exp_date'])
    refresh_token = token(query_user.id, query_user.name, token_date['access_date'])
    
    tokens = {
        'token_access': access_token,
        'token_exp': refresh_token,
        'token_type': 'Bearer'
        
    }

    return tokens
