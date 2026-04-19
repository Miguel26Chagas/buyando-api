from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only
from sqlalchemy import select, or_, and_
from app.models import User, Order, Product, ItemOrder
from app.models.order import StatusOrder

from uuid import UUID

class OrderRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def exists_order(self, seller_id: UUID, user: User):
        stmt = select(Order).where(and_(
        Order.buyer_id == user.id,
        Order.seller_id == seller_id,
        Order.status == 'PENDENT'
        )).options(selectinload(Order.list_product))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def create_order(self, seller_id: UUID, user: User):
        order = Order(
            buyer_id = user.id,
            seller_id = seller_id,
            price_total = 0.0,
            status = StatusOrder.PENDENT
        )
        try:
            self.db.add(order)
            await self.db.commit()
            await self.db.refresh(order)
            order.list_product = []
        except Exception as e:
            await self.db.rollback()
            print(f'Erro ao salvar no banco de dados: {e}')
            raise e
        return order
    
    async def check_pendent_order(self, user: User, product: Product):
        stmt = (
        select(Order)
        .filter(and_(
            Order.buyer_id == user.id,
            Order.seller_id == product.seller_id,
            Order.status == 'PENDENT'))
        .options(selectinload(Order.list_product))
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
        
    async def exist_item_order(self, product_id: UUID, order: Order):
        stmt = select(ItemOrder).where(and_(
            ItemOrder.order_id == order.id,
            ItemOrder.product_id == product_id))
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def add_item_order(self, order: Order, product: Product, data):
        order_item = ItemOrder(
            order_id = order.id,
            name_product = product.name,
            product_id = product.id,
            qtd_item = data.qtd_item,
            price = product.price * data.qtd_item
        )
        order.list_product.append(order_item)
        order.calculate_price()

        try:
            await self.db.commit()
            await self.db.refresh(order_item)
            await self.db.refresh(order)
        except Exception as e:
            await self.db.rollback()
            print(f'Erro ao salvar no banco de dados: {e}')
            raise e
        return order
    
    async def update_item_order(self, order, order_item):
        try:
            await self.db.commit()
            await self.db.refresh(order_item)
            await self.db.refresh(order)
        except Exception as e:
            await self.db.rollback()
            print(f'Erro ao salvar no banco de dados: {e}')
            raise e
        return order
            
    async def checkout_order(self, order_id: UUID, user: User):
        stmt = select(Order).where(and_(
            Order.id == order_id,
            Order.buyer_id == user.id,
            Order.status == 'PENDENT')).options(selectinload(Order.list_product))
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def get_orders(self, user: User):
        stmt = select(Order).where(Order.buyer_id == user.id).options(selectinload(Order.list_product))
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def check_status_payment(self, order_id: UUID, order: Order, user: User):
        stmt = select(Order).where(and_(
            Order.id == order_id,
            order.buyer_id == user.id,
            Order.status == 'AWAITING_PAYMENT',
        )).options(selectinload(Order.list_product))
        res = await self.db.execute(stmt)
        return res.scalar_or_none()


