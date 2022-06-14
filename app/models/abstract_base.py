from datetime import datetime
import enum

from sqlalchemy import (
    Column, DateTime, String, Enum, Integer,
)
from sqlalchemy.orm import validates
from app.core.db import Base


class ProductType(str, enum.Enum):
    offer = 'OFFER'
    category = 'CATEGORY'


class NodeBase(Base):
    __abstract__ = True

    name = Column(String(100), nullable=False)
    type = Column(Enum(ProductType), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    price = Column(Integer)
