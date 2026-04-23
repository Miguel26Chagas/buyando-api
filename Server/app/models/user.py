from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.models.types import UserRole, GenIdent

from uuid import UUID as py_UUID
from uuid import UUID as py_UUID
import uuid_utils as uuid
from datetime import datetime
class User(Base):
    __tablename__ = "user"

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_photo: Mapped[str] = mapped_column(String, nullable=True)
    public_photo_id: Mapped[str] = mapped_column(String, nullable=True)
    genre: Mapped[str] = mapped_column(GenIdent, server_default='UNDEFINED', nullable=False)

    # base_location: Mapped[Geometry] = mapped_column(Geometry('POINT', srid=4326), nullable=True)

    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), server_onupdate=func.now())
    seller: Mapped["Seller"] = relationship("Seller", back_populates="user", uselist=False)
    role: Mapped[str] = mapped_column(UserRole, server_default='BUYER', nullable=False)
    activate: Mapped[bool] = mapped_column(Boolean, server_default='true', nullable=False)