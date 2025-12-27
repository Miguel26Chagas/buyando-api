from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserSchema, LoginSchema 
from app.security import hash_password, verify_password, create_token, oaut2_form
from app.dependencies import verify_token
from app.db.database import get_db

from datetime import datetime, timezone, timedelta

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register')
async def register_user(data: UserSchema, db: Session=Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    user_exist = db.execute(stmt).scalar_one_or_none()
    if user_exist:
        raise HTTPException(
            status_code=500,
            detail='Email ou nome ja existente'
        )

    password_hash = hash_password(data.password)

    user_created = User(
        name = data.name,
        email = data.email,
        password = password_hash
    )

    try:
        db.add(user_created)
        db.commit()
        db.refresh(user_created)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f'Erro ao salvar no Banco de dados, {e}'
        )
    return {'msg': f'Usuario registado com Sucesso, {data.name}'}

@router.post('/login')
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    smt = select(User).where(or_(User.email == data.email_or_name, User.name == data.email_or_name))
    user_db = db.execute(smt).scalar_one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=400,
            detail='Senha ou email errado.'
        )
    elif not verify_password(data.password, user_db.password):
        raise HTTPException(
            status_code=400,
            detail='Senha ou email errado.'
        )
    
    token = {
        'access_token': create_token(user_db, datetime.now(timezone.utc) + timedelta(minutes=30)),
        'refresh_token': create_token(user_db, datetime.now(timezone.utc) + timedelta(days=7)),
        'token_type': 'bearer'
    }
    return token


@router.post('/login-form')
async def login_form(form: oaut2_form = Depends(), db: Session = Depends(get_db)):
    smt = select(User).where(or_(User.email == form.username, User.name == form.username))
    user_db = db.execute(smt).scalar_one_or_none()

    if not user_db:
        raise HTTPException(
            status_code=400,
            detail='Senha ou email errado.'
        )
    elif not verify_password(form.password, user_db.password):
        raise HTTPException(
            status_code=400,
            detail='Senha ou email errado.'
        )
    
    token = {
        'access_token': create_token(user_db, datetime.now(timezone.utc) + timedelta(minutes=30)),
        'token_type': 'bearer'
    }
    return token


@router.get('/refresh')
async def refresh_token(user: User = Depends(verify_token)):
    token = {
        'access_token': create_token(user, datetime.now(timezone.utc) + timedelta(minutes=30)),
        'token_type': 'bearer'
    }
    return token