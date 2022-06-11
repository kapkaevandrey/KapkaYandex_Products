from uuid import uuid4

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from app.models import NodeBase


class Node(NodeBase):
    id = Column(GUID, primary_key=True, default=uuid4)
    parent_id = Column(GUID, ForeignKey('node.id'), nullable=True)
    children = relationship("Node")

    def __repr__(self):
        return (f'Type - "{self.type}" '
                f'price - {self.price}.')

    # TODO constraint на parent_id != id
