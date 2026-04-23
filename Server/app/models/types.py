import sqlalchemy as sa
from app.db.database import Base

import enum

class UserRole(enum.Enum):
    ADMIN = 'ADMIN'
    SELLER = 'SELLER'
    BUYER = 'BUYER'

class GenIdent(enum.Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    UNISEX = 'UNISEX'
    UNDEFINED = 'UNDEFINED'

class StatusOrder(enum.Enum):
    CANCELED = 'CANCELED'
    COMPLETED = 'COMPLETED'
    AWAITING_PAYMENT = 'AWAITING_PAYMENT'
    PEMDENT = 'PEMDENT'
    PAID = 'PAID'
    REFUNED = 'REFUNED'

class CategoryDress(enum.Enum):
    HEAD = 'HEAD'
    BODY = 'BODY'
    FOOT = 'FOOT'

userrole = sa.Enum(UserRole, name= 'userrole')
genident = sa.Enum(GenIdent, name='genident')
statusorder = sa.Enum(StatusOrder, name='statusorder')
categorydress = sa.Enum(CategoryDress, name='categorydress')