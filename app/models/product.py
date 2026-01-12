from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Optional, List

import enum
import uuid
from uuid import UUID
class CategoryDress(str, enum.Enum):
    HEAD = 'head'
    FOOT = 'foot'
    BODY = 'body'

from app.db.database import Base
class Product(Base):
    __tablename__ = "product"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    seller_id: Mapped[UUID] = mapped_column(ForeignKey('seller.id'))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    qtd_stock: Mapped[int] = mapped_column(Integer, CheckConstraint('qtd_stock > 0'), default=0, nullable=True)
    detail: Mapped[str] = mapped_column(String, default='No Details')
    category: Mapped[CategoryDress] = mapped_column(SQLEnum(CategoryDress), nullable=True)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)
    photo_urls: Mapped[List['PhotosProduct']] = relationship('PhotosProduct', cascade='all, delete-orphan', back_populates='product')

class PhotosProduct(Base):
    __tablename__='photosproduct'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    photo_url: Mapped[str] = mapped_column(String, nullable=True)
    public_photo_id: Mapped[str] = mapped_column(String, nullable=True)
    product = relationship('Product', back_populates='photo_urls')
