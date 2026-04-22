from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, DateTime, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

from uuid import UUID as py_UUID
import uuid_utils as uuid
from typing import List
from datetime import datetime
class Seller(Base):
    __tablename__ = 'seller'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    number_phone: Mapped[str] = mapped_column(String, nullable=True)
    email_seller: Mapped[str] = mapped_column(String)    
    locate: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default='No Description') 
    profile_or_logo_photo_urls: Mapped[str] = mapped_column(String, nullable=False, default='No Profile Photo')

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    list_products: Mapped[List['Product']] = relationship('Product', cascade='all, delete-orphan',  back_populates='seller')


