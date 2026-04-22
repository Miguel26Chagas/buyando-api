from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, func, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

import enum
from uuid import UUID as py_UUID
from uuid import UUID as py_UUID
import uuid_utils as uuid
from datetime import datetime
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SELLER = "seller"
    BUYER = "buyer"

class GenIdent(str, enum.Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    UNDEFINED = 'Undefined'
    UNISEX = 'Unisex'

class User(Base):
    __tablename__ = "user"

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_photo: Mapped[str] = mapped_column(String, nullable=True)
    public_photo_id: Mapped[str] = mapped_column(String, nullable=True)
    genre: Mapped[GenIdent] = mapped_column(SQLEnum(GenIdent, name='genident'), server_default=GenIdent.UNDEFINED.value, nullable=False)

    # base_location: Mapped[Geometry] = mapped_column(Geometry('POINT', srid=4326), nullable=True)

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    seller: Mapped["Seller"] = relationship("Seller", back_populates="user", uselist=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name='userrole'), server_default=UserRole.BUYER.value, nullable=False)
    activate: Mapped[bool] = mapped_column(Boolean, server_default='true', nullable=False)