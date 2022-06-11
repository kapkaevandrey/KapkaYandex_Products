from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, PositiveInt, UUID4, Field

from app.models import ProductType


class NodeHistoryCreate(BaseModel):
    id: UUID4
    name: str
    parent_id: Optional[UUID4] = Field(None, alias='parentId')
    price: Optional[PositiveInt]
    type: ProductType
    date: datetime
    update_date: Optional[datetime]


class NodeHistoryUpdate(BaseModel):
    update_date: datetime

