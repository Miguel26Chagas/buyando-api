import asyncio
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependencies import verify_token, ProductForm
from app.models import User, Seller, Product, PhotosProduct
from app.schemas import ProductResponse, ProductUpdateSchema

# SERVICE
from app.services import ProductService

from typing import List
from uuid import UUID

router = APIRouter(
    prefix='/product',
    tags=['product'],
    dependencies=[Depends(verify_token)]
)

router_public = APIRouter(
    prefix='/product',
    tags=['product'],
)

@router.post('/create', response_model=ProductResponse)
async def create_product(data: ProductForm = Depends(), file_url: List[UploadFile] = File(...), user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.product(user, data, file_url)

@router.patch('/{product_id}/update', response_model=ProductResponse)
async def update_product_data(product_id:UUID, data: ProductUpdateSchema, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.update_product(product_id, data, user)

@router.delete('/{product_id}/deleting')
async def delete_product(product_id:UUID, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.delete_product(product_id, user)

@router_public.get('/all', response_model=List[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    product_service = ProductService(db)
    return await product_service.all_products()