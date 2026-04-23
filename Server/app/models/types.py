import sqlalchemy as sa
from sqlalchemy import Enum as SQLEnum
from app.db.database import Base

import enum

class UserRole(str, enum.Enum):
    pass

UserRole = sa.Enum('ADMIN', 'SELLER', 'BUYER',
                   name= 'userrole', metadata=Base.metadata)

GenIdent = sa.Enum('MALE', 'FEMALE', 'UNISEX', 'UNDEFINED',
                    name='genident', metadata=Base.metadata)

StatusOrder = sa.Enum('CANCELED', 'COMPLETED', 'AWAITING_PAYMENT', 'PEMDENT', 'PAID', 'REFUNED',
                      name='statusorder', metadata=Base.metadata)

CategoryDress = sa.Enum('HEAD', 'BODY', 'FOOT',
                      name='categorydress', metadata=Base.metadata)