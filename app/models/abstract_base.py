from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    Column, DateTime, String, Enum
)
from app.core.db import Base


class ProductType(StrEnum):
    offer = 'OFFER'
    category = 'CATEGORY'


class NodeBase(Base):
    __abstract__ = True

    name = Column(String(100), nullable=False)
    type = Column(Enum(ProductType))
    date = Column(DateTime, default=datetime.utcnow)
