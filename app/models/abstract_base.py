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
    __tableargs__ = ()

    name = Column(String(100), nullable=False)
    type = Column(Enum(ProductType))
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    price = Column(Integer)

    @validates('price', 'type')
    def validate_price_category(self, key, price, type):
        error_message = ''
        if type == ProductType.offer.value:
            if price is None:
                message = (
                    f"Field 'price' for category {ProductType.offer.value} "
                    f"cannot be None"
                )
            elif price <= 0:
                message = (
                    f"Field 'price' for category {ProductType.offer.value} "
                    f"most be greater than zero."
                )
        if type == ProductType.category.value and price is not None:
            message = (
                f"Field 'price' for category {ProductType.category.value} "
                f"must be None when create."
            )
        return price, type


# TODO написать constraints на price null if CATEGORY > 0 на date > datenow
