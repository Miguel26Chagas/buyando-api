from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas import UserResponse
from app.security import create_token, oaut2_form
from app.dependencies import verify_token, UserForm
from app.db.database import get_db
from datetime import datetime, timezone, timedelta

# SERVICES
from app.services import UserService

from typing import Optional
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', response_model=UserResponse)
async def register_user(data: UserForm = Depends(),photo_file: Optional[UploadFile] = File(None),
                        db: AsyncSession=Depends(get_db)):
    user_service = UserService(db)
    return await user_service.register(data, photo_file)

@router.post('/login')
async def login(data: oaut2_form = Depends(), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.login(data)

@router.get('/refresh')
async def refresh_token(user: User = Depends(verify_token)):
    token = {
        'access_token': create_token(user, datetime.now(timezone.utc) + timedelta(minutes=30)),
        'token_type': 'bearer'
    }
    return token