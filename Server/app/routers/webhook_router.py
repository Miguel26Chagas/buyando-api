from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db

router = APIRouter(
    prefix='whebhooks',
    tags='whebhooks'
)

@router.post('/proxypay')
async def proxypay_callback(payload: dict, db: AsyncSession = Depends(get_db)):
    custom_ref = payload.get('cr_39JYkwxk18f6AOKpQjelEoaYAjZ')