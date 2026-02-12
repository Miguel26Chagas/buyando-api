from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, SQLEnum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

import uuid
import enum
from uuid import UUID
from typing import List
from datetime import datetime

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

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(UUID, ForeignKey('user.id'), nullable=False)
    balance_available: Mapped[float] = mapped_column(Float, default=0.0)
    balance_pending: Mapped = mapped_column(Float, default=0.0)

    history_transaction: Mapped[List['HistoryTransaction']] = relationship('HistoryTransaction', cascade='all, delete-orphan', back_populates='wallet')

class HistoryTransaction(Base):
    __tablename__ = 'history_transaction'

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    wallet_id: Mapped[UUID] = mapped_column(ForeignKey('wallet.id'))
    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'), nullable=True)

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    status: Mapped[StatusTransaction] = mapped_column(SQLEnum(StatusTransaction))
    description: str = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    wallet: Mapped['Wallet'] = relationship('Wallet', back_populates='history_transaction')
