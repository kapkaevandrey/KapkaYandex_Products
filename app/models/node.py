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
    children = relationship('Node', cascade='all,delete')
    history = relationship('NodeHistory', cascade='all,delete')


    def __repr__(self):
        return (f'Type - "{self.type}" '
                f'price - {self.price}.')
