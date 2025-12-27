from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies import verify_token
from app.models import User, Product, Seller
from app.schemas import ProductSchema

router = APIRouter(
    prefix='/product',
    tags=['product'],
    dependencies=[Depends(verify_token)]
)

@router.post('/create')
async def create_product(data: ProductSchema, user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if not user.role == 'seller':
        raise HTTPException(
            status_code=400,
            detail='Você precisa criar sua conta vendedor pra vender produtos.'
        )
    
    stmt = select(Seller).where(Seller.user_id == user.id)
    who_is_seller = db.execute(stmt).scalar_one()

    product = Product(
        name = data.name,
        seller_id = who_is_seller.id,
        price = data.price,
        qtd = data.qtd,
        detail = data.detail,
        category = data.category,
        disponible = data.disponible
    )
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
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