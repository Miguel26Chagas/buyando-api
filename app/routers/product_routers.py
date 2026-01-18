import asyncio
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.dependencies import verify_token, ProductForm
from app.models import User, Seller, Product, PhotosProduct
from app.schemas import ProductResponse, ProductUpadate
from app.cloudinary import cloudinary_uploader

from typing import List
from uuid import UUID

router = APIRouter(
    prefix='/product',
    tags=['product'],
    dependencies=[Depends(verify_token)]
)

@router.post('/create', response_model=ProductResponse)
async def create_product(data: ProductForm = Depends(), file_url: List[UploadFile] = File(...), user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    if not user.role == 'seller':
        raise HTTPException(
            status_code=403,
            detail='Você precisa criar sua conta vendedor pra vender produtos.'
        )
    
    stmt = select(Seller).where(Seller.user_id == user.id)
    res = await db.execute(stmt)
    is_seller = res.scalar_one_or_none()
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
            return await loop.run_in_executor(None, lambda: cloudinary_uploader.upload(content))

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
    return product

@router.get('/list')
async def list_products(user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Seller).where(Seller.user_id == user.id)
    res = await db.execute(stmt)
    seller = res.scalar_one_or_none()

    if not user.role == 'seller':
        raise HTTPException(status_code=400, detail='Voce Nao vende nada')
    
    stmt2 = select(Product).where(Product.seller_id == seller.id)
    res2 = await db.execute(stmt2)
    products = res2.scalars()

    if not products:
        raise HTTPException(status_code=4003, detail='Sem produtos a venda')
    return products

@router.patch('/{product_id}/update')
async def update_product_data(product_id:UUID, data: ProductUpadate, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    if not user.role == 'seller':
        raise HTTPException(status_code=403, detail='Voce nao tem permissao pra isto')

    stmt = select(Product).where(Product.id == product_id)
    res = await db.execute(stmt)
    product = res.scalar_one_or_none()
    stmt2 = select(Seller).where(Seller.id == product.seller_id)
    res2 = await db.execute(stmt2)
    seller = res2.scalar_one_or_none
    
    if not product:
        raise HTTPException(status_code=400, detail='Produto Nao encontrado')
    elif not seller.user_id == user.id:
        raise HTTPException(status_code=403, detail='Negado, voce na pode alterar esse produto')

    