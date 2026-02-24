from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from app.dependencies import verify_token
from app.models import User
from app.schemas import PasswordSchema, UserUpdate, UserMe
from app.security import verify_password, hash_password
from app.db.database import get_db
from app.cloudinary import cloudinary_uploader

import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix='/user',
    tags=['user'],
    dependencies=[Depends(verify_token)]
)

@router.get('/me', response_model = UserMe)
async def me(user: User = Depends(verify_token)):
    return user

@router.patch('/update/password')
async def update_password(data:PasswordSchema, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    password = verify_password(data.password, user.password)
    if not password:
        raise HTTPException(
            status_code=400,
            detail='Senha Incorreta'
        )
    user.password = hash_password(data.new_password)

    try:
        await db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao salvar no Banco de Dados, {e}'
        )
    return {'msg': 'Senha alterada com sucesso!'}

@router.patch('/update/data')
async def update_data(data: UserUpdate, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):

    if not data.name == None or '':
        user.name = data.name
    elif not data.email == None or '':
        user.email = data.email
    else:
        raise HTTPException(status_code=400, detail='Nada aqui pra salvar')

    try:
        await db.commit()
    except Exception as e:
        db.rollback()
        raise Exception(
            status_code = 500,
            detail = f'Erro ao atualizar dados!, {e}'
        )
    return {'msg': 'Ação concluida!'}

@router.post('/add_photo')
async def add_photo_user(user: User = Depends(verify_token), photo_file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    old_public_photo_id = user.public_photo_id

    loop = asyncio.get_running_loop()
    if photo_file:
        try:
            upload_result = await loop.run_in_executor(
                None,
                lambda: cloudinary_uploader.upload(photo_file.file)
            )
            secure_url = upload_result['secure_url']
            public_id = upload_result['public_id']
        except Exception as e:
            raise HTTPException(
                status_code=409,
                detail=f'Erro No cloudinary, {e}'
            )
    else:
        raise HTTPException(
            status_code=400,
            detail='Por Favor Insira uma Imagem'
        )

    user.profile_photo = secure_url
    user.public_photo_id = public_id

    try:
        db.add(user)
        await db.commit()

        if old_public_photo_id:
            await loop.run_in_executor(None, lambda: cloudinary_uploader.destroy(old_public_photo_id))
        await db.refresh(user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao salvar no Banco de dados ,{e}'
        )
 
    message = "Foto alterada com sucesso" if old_public_photo_id else "Foto adicionada com sucesso"
    return {
        "msg": message,
        "url": user.profile_photo
    }