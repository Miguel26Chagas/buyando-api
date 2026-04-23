from sqlalchemy import ForeignKey, String, Integer, Boolean, func, Numeric
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from typing import Optional, List

from uuid import UUID as py_UUID
import uuid_utils as uuid
from datetime import datetime
from decimal import Decimal

from app.db.database import Base
from app.models.types import CategoryDress, GenIdent

class Product(Base):
    __tablename__ = "product"

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    qtd_stock: Mapped[int] = mapped_column(Integer, CheckConstraint('qtd_stock > 0'), default=1, nullable=True)
    detail: Mapped[str] = mapped_column(String, default='No Details')

    category: Mapped[str] = mapped_column(CategoryDress, nullable=True)
    target_genre: Mapped[str] = mapped_column(GenIdent, server_default='UNDEFINED')
    disponible: Mapped[bool] = mapped_column(Boolean, server_default='true')
    photo_urls: Mapped[List['PhotosProduct']] = relationship('PhotosProduct', cascade='all, delete-orphan', back_populates='product')
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())

    seller: Mapped['Seller'] = relationship('Seller', back_populates='list_products')

class PhotosProduct(Base):
    __tablename__='photosproduct'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    public_photo_id: Mapped[str] = mapped_column(String, nullable=True)
    product = relationship('Product', back_populates='photo_urls')

class Category (Base):
    __tablename__ = 'category'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    