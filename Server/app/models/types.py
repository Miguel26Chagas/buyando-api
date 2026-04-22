import sqlalchemy as sa
from app.db.database import Base

UserRole = sa.Enum('ADMIN', 'SELLER', 'BUYER',
                   name= 'userrole', metadata=Base.metadata)

GeniIdent = sa.Enum('MALE', 'FEMALE', 'UNISEX', 'UNDEFINED',
                    name='geniident', metadata=Base.metadata)

StatusOrder = sa.Enum('CANCELED', 'COMPLETED', 'AWAITING_PAYMENT', 'PEMDENT', 'PAID', 'REFUNED',
                      name='statusorder', metadata=Base.metadata)

CategoryDress = sa.Enum('HEAD', 'BODY', 'FOOT'
                      name='categorydress', metadata=Base.metadata)