from uuid import uuid4

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, validates

from app.models import NodeBase
from app.models import ProductType


class Node(NodeBase):
    __tableargs__ = (
        CheckConstraint('id != parent_id', 'id_not_parent_id'),
    )

    id = Column(GUID, primary_key=True, default=uuid4)
    parent_id = Column(GUID, ForeignKey('node.id'), nullable=True)
    children = relationship("Node")

    @validates('parent_id', 'type')
    def validate_parent_category(self, key, parent_id, type):
        if parent_id is None and type == ProductType.offer.value:
            raise ValueError(
                f"Node type {ProductType.offer.value} most have "
                f"not null 'field parent_id'"
            )
        return parent_id, type

    def __repr__(self):
        return (f'Type - "{self.type}" '
                f'price - {self.price}.')
