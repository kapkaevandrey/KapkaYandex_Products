from datetime import datetime
from typing import Optional, List

from pydantic import (
    BaseModel, NonNegativeInt, UUID4, Field, validator, root_validator,
)

from app.models import ProductType


class NodeBase(BaseModel):
    id: UUID4
    name: str
    parent_id: Optional[UUID4]
    price: Optional[NonNegativeInt]
    type: ProductType


class NodeCreate(NodeBase):
    @validator('name')
    def value_cannot_be_none(cls, value):
        if not value or value is None:
            raise ValueError(
                'Value cannot be None'
            )
        return value

    @root_validator
    def check_price_type_category(cls, values):
        if values['type'] == ProductType.offer.value:
            if 'price' in values and values['price'] is None:
                raise ValueError(
                    f'Price for category {ProductType.offer.value}'
                    f' cannot be None'
                )
        elif values['type'] == ProductType.category.value:
            if 'price' in values and values['price'] is not None:
                raise ValueError(
                    f'Price for category {ProductType.category.value}'
                    f' must be None when create'
                )
        if values['id'] == values['parent_id']:
            raise ValueError(
                f'A node cannot be a parent to itself '
                f'id={values["id"]} parent_id={values["parent_id"]}'
            )
        return values


class NodeListCreate(BaseModel):
    items: List[NodeCreate]
    date: datetime = Field(alias='updateDate')

    @validator('date')
    def date_cannot_be_greater_then_now(cls, value):
        if value > datetime.now(tz=value.tzinfo):
            raise ValueError(
                f'Date cannot be greater the current time '
                f'{datetime.now(tz=value.tzinfo).isoformat()}'
            )
        return value


class NodeUpdate(NodeCreate):
    pass


class NodeRead(NodeBase):
    date: datetime
    children: Optional[List]

    class Config:
        orm_mode = True
