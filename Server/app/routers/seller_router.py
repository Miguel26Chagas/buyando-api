from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Seller, Product
from app.schemas import SellerSchema, ProductResponse
from app.dependencies import verify_token
from app.db.database import get_db

from typing import List

router = APIRouter(
    prefix='/seller',
    tags=['seller'],
    dependencies=[Depends(verify_token)]
)

@router.post('/active')
async def seller_active(data: SellerSchema, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Seller).where(Seller.user_id == user.id)
    res = await db.execute(stmt)
    seller_exist = res.scalar_one_or_none()

    if seller_exist:
        raise HTTPException(
            status_code=400,
            detail='Este usuario ja tem ativo uma conta vendedor'
        )
    if data.email_seller == None or '':
        data.email_seller = user.email

    seller_active = Seller(
        seller_name = data.seller_name,
        locate = data.locate,
        user_id = user.id,
        number_phone = data.number_phone,
        email_seller = data.email_seller,
        description = data.description
    )

    user.role = 'SELLER'

    try:
        db.add(seller_active)
        await db.commit()
        await db.refresh(seller_active)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail = 'Ocorreu um erro ao salvar no banco de dados'
        )
    return {'msg': f'Conta Vendedor Ativo!'}

@router.get('/list-products/me', response_model=List[ProductResponse])
async def list_products(user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Seller).where(Seller.user_id == user.id)
    res = await db.execute(stmt)
    seller = res.scalar_one_or_none()

    if not user.role == 'seller':
        raise HTTPException(status_code=400, detail='Voce Nao vende nada')
    
    stmt2 = select(Product).where(Product.seller_id == seller.id)
    res2 = await db.execute(stmt2)
    products = res2.scalars().all()

    if not products:
        raise HTTPException(status_code=403, detail='Sem produtos a venda')
    return products