from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, SQLEnum, DateTime, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

import enum
from uuid import UUID as py_UUID
import uuid_utils as uuid
from typing import List
from datetime import datetime
from decimal import Decimal

class TransactionType(str, enum.Enum):
    SALE = 'SALE'
    WITHDRAW = 'WITHDRAW'
    REFUND = 'REFUND'
    COMISSION = 'COMISSION'

class StatusTransaction(str, enum.Enum):
    HELD = 'HELD' #congelado
    COMPLETED = 'COMPLETED' #Concluido
    EXPIRED = 'EXPIRED' #Expirou
    CANCELLED = 'CANCELLED' #Cancelado
    REFUNDED = 'REFUNDED' #Devolvido

class Wallet(Base):
    __tablename__ = 'wallet'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    balance_available: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.0)
    balance_pending: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.0)

    history_transaction: Mapped[List['HistoryTransaction']] = relationship('HistoryTransaction', cascade='all', back_populates='wallet')

class HistoryTransaction(Base):
    __tablename__ = 'history_transaction'

    id: Mapped[py_UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid7)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    balance_after: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    status: Mapped[StatusTransaction] = mapped_column(SQLEnum(StatusTransaction))
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    wallet: Mapped['Wallet'] = relationship('Wallet', back_populates='history_transaction')
