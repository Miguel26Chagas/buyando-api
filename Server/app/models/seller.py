from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

import uuid
from uuid import UUID
from typing import List
class Seller(Base):
    __tablename__ = 'seller'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), index=True)
    seller_name: Mapped[str] = mapped_column(String, nullable=False)
    number_phone: Mapped[str] = mapped_column(String, nullable=True)
    email_seller: Mapped[str] = mapped_column(String)    
    locate: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default='No Description') 
    profile_or_logo_photo_urls: Mapped[str] = mapped_column(String, nullable=False, default='No Profile Photo')

    list_products: Mapped[List['Product']] = relationship('Product', cascade='all, delete-orphan',  back_populates='seller')


