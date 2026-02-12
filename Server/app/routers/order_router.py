from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.dependencies import verify_token
from app.db.database import get_db
from app.models import Order, Product, User, ItemOrder, Seller
from app.schemas import ItemOrderSchema, OrderResponse, ItemOrderResponse

from app.models.order import StatusOrder

from uuid import UUID
from typing import List

router = APIRouter(
    prefix='/order',
    tags=['order'],
    dependencies=[Depends(verify_token)]
)

@router.post('/buying/{seller_id}', response_model=OrderResponse)
async def order(seller_id:UUID, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):    
    try:
        stmt = select(Seller).where(Seller.id == seller_id)
        res = await db.execute(stmt)
        seller = res.scalar_one_or_none()
        stmt2 = select(Product.id).where(Product.seller_id == seller_id).limit(1)
        res2 = await db.execute(stmt2)
        products = res2.scalar() is not None

        if not seller:
            raise HTTPException(status_code=403, detail='Este Usuario Nao e Vendedor!')
        elif not products:
            raise HTTPException(status_code=404, detail="Este vendedor não possui produtos.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Erro na consulta, {e}')
    
    stmt3 = select(Order).where(and_(
        Order.buyer_id == user.id,
        Order.seller_id == seller_id,
        Order.status == 'PENDENT'
    )).options(selectinload(Order.list_product))
    res3 = await db.execute(stmt3)
    order = res3.scalar_one_or_none()
    if not order:
        order = Order(
            buyer_id = user.id,
            seller_id = seller_id,
            price_total = 0.0,
            status = StatusOrder.PENDENT
        )
        try:
            db.add(order)
            await db.commit()
            await db.refresh(order)
            order.list_product = []
        except Exception as e:
            await db.rollback()
            print(f'DEBUG ERROR:{e}')
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
        
    return order

@router.post('/buying/{product_id}/item', response_model=ItemOrderResponse)
async def item_order(product_id:UUID, data:ItemOrderSchema, user: User = Depends(verify_token),db: AsyncSession = Depends(get_db)):
    stmt = select(Product).filter(Product.id == product_id)
    res = await db.execute(stmt)
    product = res.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=400,
            detail='Este Produto Nao Foi encontrado'
        )
    
    stmt2 = (
        select(Order)
        .filter(and_(
            Order.buyer_id == user.id,
            Order.seller_id == product.seller_id,
            Order.status == 'PENDENT'))
        .options(selectinload(Order.list_product))
    )
    res2 = await db.execute(stmt2)
    order = res2.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=400,
            detail='Faca um pedido ao dono desse produto'
        )
    if not order.buyer_id == user.id:
        raise HTTPException(status_code=403, detail='Este Pedido Nao e seu!')

    stmt3 = select(ItemOrder).where(and_(
        ItemOrder.order_id == order.id,
        ItemOrder.product_id == product_id))
    res3 = await db.execute(stmt3)
    exist_item_product = res3.scalars().first()

    if data.qtd_item <= 0:
        raise HTTPException(status_code=400, detail='Por favor insira uma quantidade valida')
    
    try:
        if exist_item_product:
            if product.qtd_stock < data.qtd_item:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
            exist_item_product.qtd_item = data.qtd_item
            exist_item_product.price = product.price * data.qtd_item
            order_item = exist_item_product
        else:
            if product.qtd_stock <= 0 or product.disponible != True:
                raise HTTPException(
                    status_code=400,
                    detail=f'Não ha {product.name} disponiveis no momento.'
                )
            if product.qtd_stock < data.qtd_item:
                raise HTTPException(
                    status_code=400,
                    detail=f'Nao Ha essa quantidade no stock, só ha {product.qtd_stock}'
                )
            order_item = ItemOrder(
                order_id = order.id,
                name_product = product.name,
                product_id = product.id,
                qtd_item = data.qtd_item,
                price = product.price * data.qtd_item
            )
            order.list_product.append(order_item)
        order.calculate_price()
        await db.commit()
        await db.refresh(order_item)
        await db.refresh(order)
    except Exception as e:
        await db.rollback()
        print(e)
        raise HTTPException(
        status_code=500,
        detail=f'Erro ao solicitar, {e}'
    )

    return order_item

@router.post('/{order_id}/checkout', response_model=OrderResponse)
async def checkout_order(order_id:UUID, user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Order).where(and_(
        Order.id == order_id,
        Order.buyer_id == user.id,
        Order.status == 'PENDENT')).options(selectinload(Order.list_product))
    res = await db.execute(stmt)
    order = res.scalar_one_or_none()

    if not order or not order.list_product:
        raise HTTPException(status_code=400, detail='Compra Nao existente ou Sem produtos pra processar')
    products = order.list_product

    try:
        for item in products:
            stmt2 = select(Product).where(Product.id == item.product_id).with_for_update()
            res2 = await db.execute(stmt2)
            product = res2.scalar_one_or_none()
            if not product or product.disponible == False:
                raise HTTPException(status_code=400, detail=f'Infelizmente nao ha mais {item.name_product} produto no stock')
            if product.qtd_stock < item.qtd_item:
                raise HTTPException(status_code=400, detail=f'Lamento, so restam {product.qtd_stock} no stock.')
            product.qtd_stock -= item.qtd_item

        order.status = StatusOrder.AWAITING_PAYMENT
        await db.commit()
        await db.refresh(order)
    except HTTPException as http_e:
        await db.rollback()
        raise http_e
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail='Erro na operacao')
    
    return order

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
     
@router.get('/order/me', response_model=List[OrderResponse])
async def my_orders(user: User = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    stmt = select(Order).where(Order.buyer_id == user.id).options(selectinload(Order.list_product))
    res = await db.execute(stmt)
    orders = res.scalars().all()

    if not orders:
        raise HTTPException(status_code=400, detail='Sem Pedidos ou compras')
    return orders
