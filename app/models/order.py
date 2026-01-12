from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List
from app.db.database import Base

import enum
import uuid
from uuid import UUID
class StatusOrder(enum.Enum):
    CANCELED = 'CANCELED'
    SUCCESSED = 'SUCCESSED'
    PENDENT = 'PENDENT'

class Order(Base):
    __tablename__ = 'order'

    id: Mapped[UUID] = mapped_column(Integer, primary_key=True, index=True, default=uuid.uuid4)
    buyer_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), nullable=True, index=True)
    seller_id: Mapped[UUID] = mapped_column(ForeignKey('seller.id'),)
    price_total: Mapped[float] = mapped_column(Float, CheckConstraint('price_total >= 0'), nullable=True, default=0)
    status: Mapped[StatusOrder] = mapped_column(SQLEnum(StatusOrder), default=StatusOrder.PENDENT)

    list_product: Mapped[List['ItemOrder']] =  relationship('ItemOrder', back_populates='order', cascade='all, delete')

    def calculate_price(self,):
        self.price_total = sum(item.price for item in self.list_product)

class ItemOrder(Base):
    __tablename__ = 'item_order'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'))
    name_product: Mapped[str] = mapped_column(String, nullable=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'), nullable=True)
    qtd_item: Mapped[int] = mapped_column(Integer, CheckConstraint('qtd_item > 0'), default=1)
    price: Mapped[float] = mapped_column(Float,CheckConstraint('price >= 0'), nullable=True)

    order: Mapped['Order'] = relationship('Order', back_populates='list_product', cascade='all, delete')
