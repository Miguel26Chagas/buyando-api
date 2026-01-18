from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.dependencies import verify_token
from app.db.database import get_db
from app.models import Order, Product, User, ItemOrder
from app.schemas import ItemOrderSchema

from uuid import UUID

router = APIRouter(
    prefix='/order',
    tags=['order'],
    dependencies=[Depends(verify_token)]
)

@router.post('/buying/{seller_id}')
async def order(seller_id:UUID, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):    
    try:
        stmt = select(Product).where(Product.seller_id == seller_id)
        res = await db.execute(stmt)
        products = res.scalars().all()
        if not products:
            raise HTTPException(status_code=404, detail="Este vendedor não possui produtos.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Erro na consulta, {e}')

    if not products:
        raise HTTPException(
            status_code=400,
            detail='Produtos Nao encontrado'
        )
    
    stmt2 = select(Order).where(
        Order.buyer_id == user.id,
        Order.seller_id == seller_id,
        Order.status == 'PENDENT'
    ).options(selectinload(Order.list_product))

    res = await db.execute(stmt2)
    order = res.scalars().all()
    if_new = False
    if not order:
        order = Order(buyer_id = user.id, seller_id = seller_id)

        try:
            db.add(order)
            await db.commit()
            await db.refresh(order)
            if_new=True
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail='Erro ao fazer a compra'
            )
    
    return {
        'msg': 'Solicitacao da Compra atualizada' if not if_new else 'Novo pedido criado',
        'order_id': order.id,
        'status': order.status,
        'produtos': order.list_product
    }

@router.post('/buying/{product_id}/item')
async def item_order(product_id:UUID, data:ItemOrderSchema, db: Session = Depends(get_db)):
    stmt = select(Product).filter(Product.id == product_id)
    product = db.execute(stmt).scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=400,
            detail='Este Produto Nao Foi encontrado'
        )
    if product.qtd_stock <= 0 or product.disponible != True:
        raise HTTPException(
            status_code=400,
            detail=f'Nao ha {product.name} disponiveis no momento.'
        )
    if product.qtd_stock < data.qtd_item:
        raise HTTPException(
            status_code=400,
            detail=f'Nao Ha essa quantidade no stock, só ha {product.qtd_stock}'
        )
    
    stmt = select(Order).filter(Order.id == data.order_id)
    order = db.execute(stmt).scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=400,
            detail='Esta solicitacao ainda nao foi feito'
        )
    order_item = ItemOrder(
        order_id = data.order_id,
        name_product = product.name,
        product = product.id,
        qtd_item = data.qtd_item,
        price = product.price * data.qtd_item
    )

    try:
        order.list_product.append(order_item)
        order.calculate_price()
        product.qtd_stock -= data.qtd_item
        db.commit()
        db.refresh(order_item)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f'Erro ao solicitar, {e}'
        )
    return {'msg': 'Item Adicionado a sua Compra'}