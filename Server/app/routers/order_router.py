from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.dependencies import verify_token
from app.db.database import get_db
from app.models import Order, Product, User, ItemOrder, Seller
from app.schemas import ItemOrderSchema, OrderResponse, ItemOrderResponse

# SERVICE
from app.services import OrderService

from uuid import UUID
from typing import List

router = APIRouter(
    prefix='/order',
    tags=['order'],
    dependencies=[Depends(verify_token)]
)

@router.post('/buying/{seller_id}', response_model=OrderResponse)
async def order(seller_id:UUID, user: User = Depends(verify_token),db: AsyncSession = Depends(get_db)):    
   order_service = OrderService(db)
   return await order_service.order(seller_id, user)

@router.post('/buying/{product_id}/item', response_model=OrderResponse)
async def item_order(product_id:UUID, data:ItemOrderSchema, user: User = Depends(verify_token),db: AsyncSession = Depends(get_db)):
    order_service = OrderService(db)
    return await order_service.add_item_order(product_id, data, user)

@router.post('/{order_id}/checkout', response_model=OrderResponse)
async def checkout_order(order_id:UUID, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    order_service = OrderService(db)
    return await order_service.checkout_order(order_id, user)

@router.post('/{order_id}/confirm_payment')
async  def confirm_delivery(order_id: UUID, user = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Order).where(and_(
        Order.id == order_id,
        order.buyer_id == user.id,
        Order.status == 'AWAITING_PAYMENT',
    )).options(selectinload(Order.list_product))
    res = await db.execute(stmt)
    order = res.scalar_or_none()

    if not order or not order.status == 'AWAITING_PAYMENT':
        raise HTTPException(status_code=400, detail='Nao ha compra a ser pago!')
     
@router.get('/me', response_model=List[OrderResponse])
async def my_orders(user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    order_service = OrderService(db)
    return await order_service.list_orders(user) 
