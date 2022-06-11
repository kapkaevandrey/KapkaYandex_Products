import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import (
    BaseModel, NonNegativeInt, UUID4, Field, validator, root_validator,
)

from app.models import ProductType


class NodeCreate(BaseModel):
    id: UUID4
    name: str
    parent_id: Optional[UUID4]
    price: Optional[NonNegativeInt]
    type: ProductType

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
        return values


class NodeListCreate(BaseModel):
    items: List[NodeCreate]
    date: datetime = Field(alias='updateDate')


class NodeUpdate(NodeCreate):
    pass


class NodeRead(NodeCreate):
    date: datetime
    children: List['NodeRead']


parent_id = uuid.uuid4()
second_parent_id = uuid.uuid4()
third_parent_id = uuid.uuid4()
four_parent_id = uuid.uuid4()

date = datetime.utcnow()

node_1 = NodeCreate(
    id=parent_id, name='first_category', parentId=None,
    price=None, type="OFFER", date=date
)

# node_2 = NodeCreate(
#     id=second_parent_id, name='second_category', parentId=parent_id,
#     price=None, type="CATEGORY", date=date
# )
# node_3 = NodeCreate(
#     id=third_parent_id, name='third_category', parentId=parent_id,
#     price=None, type="CATEGORY", date=date
# )
# node_4 = NodeCreate(
#     id=third_parent_id, name='third_category', parentId=parent_id,
#     price=None, type="CATEGORY", date=date
# )

