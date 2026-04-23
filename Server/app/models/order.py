from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Numeric
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from typing import List, Optional
from app.db.database import Base
from app.models.types import StatusOrder

from uuid import UUID as py_UUID
import uuid_utils as uuid
from datetime import datetime
from decimal import Decimal
class Order(Base):
    __tablename__ = 'order'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    seller_id: Mapped[UUID] = mapped_column(ForeignKey('seller.id'),)
    price_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), CheckConstraint('price_total >= 0'), default=0)
    status: Mapped[str] = mapped_column(StatusOrder, server_default='PENDENT')
    secret_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    delivery_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    list_product: Mapped[List['ItemOrder']] =  relationship('ItemOrder', back_populates='order', cascade='all, delete')

    def calculate_price(self,):
        self.price_total = sum(item.price for item in self.list_product)

class ItemOrder(Base):
    __tablename__ = 'item_order'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    name: Mapped[str] = mapped_column(String)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'))
    name_product: Mapped[str] = mapped_column(String, nullable=True)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'), nullable=True)
    qtd_item: Mapped[int] = mapped_column(Integer, CheckConstraint('qtd_item > 0'), default=1)
    each_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), CheckConstraint('price >= 0'))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), CheckConstraint('price >= 0'), nullable=True)

    name_product_snapshot: Mapped[str] = mapped_column(String)
    price_snapshot: Mapped[Decimal] = mapped_column(Numeric(10, 2), CheckConstraint('price >= 0'), nullable=False, default=0.0)

    order: Mapped['Order'] = relationship('Order', back_populates='list_product', cascade='all, delete')
