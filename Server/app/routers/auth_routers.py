import asyncio
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserResponse
from app.security import hash_password, verify_password, create_token, oaut2_form
from app.dependencies import verify_token, UserForm
from app.db.database import get_db
from app.cloudinary import cloudinary_uploader
from datetime import datetime, timezone, timedelta

from typing import Optional
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', response_model=UserResponse)
async def register_user(data: UserForm = Depends(), photo_file: UploadFile = File(None), db: AsyncSession=Depends(get_db)):
    stmt = select(User).where(or_(User.email == data.email, User.name == data.name))
    res = await db.execute(stmt)
    user_exist = res.scalar_one_or_none()
    if user_exist:
        raise HTTPException(
            status_code=409,
            detail='Email ou nome ja existente'
        )

    secure_url = 'No Profile Photo'
    public_id = None
    if photo_file:
        try:
            loop = asyncio.get_running_loop()
            upload_result = await loop.run_in_executor(
                None,
                lambda: cloudinary_uploader.upload(photo_file.file)
            )
            secure_url = upload_result['secure_url']
            public_id = upload_result['public_id']
        except Exception as e:
            raise HTTPException(status_code=409, detail=f'Erro no Cloudinary, {e}')

    password_hash = hash_password(data.password)

    user_created = User(
        name = data.name,
        email = data.email,
        password = password_hash,
        profile_photo = secure_url,
        public_photo_id = public_id
    )

    try:
        db.add(user_created)
        await db.commit()
        await db.refresh(user_created)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f'Erro ao salvar no Banco de dados, {e}'
        )
    return user_created

@router.post('/login')
async def login(data: oaut2_form = Depends(), db: AsyncSession = Depends(get_db)):
    smt = select(User).where(or_(User.email == data.username, User.name == data.username))
    res = await db.execute(smt)
    user_db = res.scalar_one_or_none()

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
        'token_type': 'bearer',
    }
    return token

@router.get('/refresh')
async def refresh_token(user: User = Depends(verify_token)):
    token = {
        'access_token': create_token(user, datetime.now(timezone.utc) + timedelta(minutes=30)),
        'token_type': 'bearer'
    }
    return token