from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

import enum
 
class CategoryDress(str, enum.Enum):
    HEAD = 'head'
    FOOT = 'foot'
    BODY = 'body'

from app.db.database import Base

class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[int] = mapped_column(String, index=True, nullable=False)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey('seller.id'))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    qtd: Mapped[int] = mapped_column(Integer, default=0)
    detail: Mapped[str] = mapped_column(String, default='No Details')
    category: Mapped[CategoryDress] = mapped_column(SQLEnum(CategoryDress), nullable=True)
    disponible: Mapped[bool] = mapped_column(Boolean, default=True)

