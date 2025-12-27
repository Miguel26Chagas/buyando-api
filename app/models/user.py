from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.BUYER, nullable=False)
    activate: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)