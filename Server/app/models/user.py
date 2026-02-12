from sqlalchemy import ForeignKey, String, Integer, Boolean, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

import enum
import uuid
from uuid import UUID

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_photo: Mapped[str] = mapped_column(String, nullable=False, default='No Profile Photo')
    public_photo_id: Mapped[str] = mapped_column(String, nullable=True, default=None)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.BUYER, nullable=False)
    activate: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)