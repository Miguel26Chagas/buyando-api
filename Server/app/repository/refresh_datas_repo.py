from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Order, Product

class RefreshDataRepo():
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_rollback(self):
        pass

    async def refresh_order(self, order: Order):
        try:
            await self.db.commit()
            await self.db.refresh(order)
        except Exception as e:
            await self.db.rollback()
            raise e
        return print('Rrefresh to DB')
    
    async def refresh_product(self, product: Product):
        try:
            await self.db.commit()
            await self.db.refresh(product)
        except Exception as e:
            await self.db.rollback()
            raise e
        return print('Rrefresh to DB')