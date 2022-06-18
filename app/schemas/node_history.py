from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, PositiveInt, UUID4, Field

from app.models import ProductType


class NodeHistoryCreate(BaseModel):
    node_id: UUID4 = Field(alias='id')
    name: str
    parent_id: Optional[UUID4] = Field(None, alias='parentId')
    price: Optional[PositiveInt]
    type: ProductType
    date: datetime
    update_date: Optional[datetime]


class NodeHistoryUpdate(BaseModel):
    update_date: datetime


class NodeHistoryRead(BaseModel):
    id: UUID4
    name: str
    parent_id: Optional[UUID4] = Field(None, alias='parentId')
    price: Optional[PositiveInt]
    type: ProductType
    date: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(
                timespec='milliseconds'
            ) + 'Z',
        }


class NodeHistoryListRead(BaseModel):
    items: List[NodeHistoryRead]
