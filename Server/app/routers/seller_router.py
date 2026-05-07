from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Seller, Product
from app.schemas import SellerSchema, ProductResponse, SellerResponseBase
from app.dependencies import verify_token
from app.db.database import get_db

# SERVICE
from app.services import SellerService, ProductService

from typing import List

router = APIRouter(
    prefix='/seller',
    tags=['seller'],
    dependencies=[Depends(verify_token)]
)

@router.post('/active', response_model=SellerResponseBase)
async def seller_active(data: SellerSchema, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
   seller_service = SellerService(db)
   return await seller_service.seller_active(user, data)

@router.get('/list-products/me', response_model=List[ProductResponse])
async def list_products(user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.all_products()
