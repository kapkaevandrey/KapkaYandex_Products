from datetime import datetime
import enum

from sqlalchemy import (
    Column, DateTime, String, Enum, Integer
)
from app.core.db import Base


class ProductType(str, enum.Enum):
    offer = 'OFFER'
    category = 'CATEGORY'


class NodeBase(Base):
    __abstract__ = True

    name = Column(String(100), nullable=False)
    type = Column(Enum(ProductType))
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    price = Column(Integer)

# TODO написать constraints на price null if CATEGORY > 0 на date > datenow
