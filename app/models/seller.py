from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Seller(Base):
    __tablename__ = 'seller'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), index=True)
    seller_name: Mapped[str] = mapped_column(String, nullable=False)
    number_phone: Mapped[str] = mapped_column(String, nullable=True)
    email_seller: Mapped[str] = mapped_column(String)    
    locate: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default='No Description') 

