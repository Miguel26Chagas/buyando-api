import asyncio
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependencies import verify_token, ProductForm
from app.models import User, Seller, Product, PhotosProduct
from app.schemas import ProductResponse
from app.cloudinary import cloudinary_uploader

from typing import List

router = APIRouter(
    prefix='/product',
    tags=['product'],
    dependencies=[Depends(verify_token)]
)

@router.post('/create', response_model=ProductResponse)
async def create_product(data: ProductForm = Depends(), file_url: List[UploadFile] = File(), user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    if not user.role == 'seller':
        raise HTTPException(
            status_code=403,
            detail='Você precisa criar sua conta vendedor pra vender produtos.'
        )
    
    stmt = select(Seller).where(Seller.user_id == user.id)
    is_seller = await db.execute(stmt).scalar_one_or_none()
    if not is_seller:
        raise HTTPException(
            status_code=403,
            detail='Usuario nao e vendedor'
        )

    photos = []
    loop = asyncio.get_running_loop()
    try:
        async def upload_wrapper(file):
            content = await file.read()
            return await loop.run_in_executor(None, lambda: cloudinary_uploader(content))

        responses = await asyncio.gather(*(upload_wrapper(f) for f in file_url))
        photos = [
            PhotosProduct(
                photo_url = res['secure_url'],
                public_photo_id=res['public_id']
            )
            for res in responses
        ]
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail = f'Por favor, insira uma imagem do seu produto, {e}'
        )

    product = Product(
        name = data.name,
        seller_id = is_seller.id,
        price = data.price,
        qtd_stock = data.qtd,
        detail = data.detail,
        category = data.category,
        disponible = data.disponible,
        photo_urls = photos
    )
    
    try:
        db.add(product)
        await db.commit()
        await db.refresh(product)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Aconteceu um erro ao salvar no Banco de dados, {e}'
        )
    return {
        'msg': 'Produto criado com sucesso',
        'nome': data.name,
        'price': data.price
    }