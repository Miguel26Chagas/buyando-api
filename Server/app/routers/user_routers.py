from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, BackgroundTasks
from app.dependencies import verify_token
from app.models import User
from app.schemas import PasswordSchema, UserUpdate, UserMe
from app.security import verify_password, hash_password
from app.db.database import get_db
from app.cloudinary import cloudinary_uploader

import asyncio

# SERVICE
from app.services import UserService

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
async def update_password(data:PasswordSchema,
                          user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.update_password(data, user)

@router.patch('/update/data')
async def update_data(data: UserUpdate,
                      user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    await user_service.update_data(data, user)
   
    return {'msg': 'Ação concluida!'}

@router.patch('/add_photo')
async def add_photo_user(background_tasks: BackgroundTasks,
                         user: User = Depends(verify_token),photo_file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.add_photo(background_tasks, user, photo_file)