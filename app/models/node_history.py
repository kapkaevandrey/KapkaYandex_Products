from app.models import NodeBase

from sqlalchemy import (
    Column, CheckConstraint, DateTime, ForeignKey,
    Integer,
)
from fastapi_users_db_sqlalchemy import GUID


class NodeHistory(NodeBase):
    __tableargs__ = (
        CheckConstraint('date < update_date', 'date_lower_update_date'),
    )

    id = Column(Integer, primary_key=True)
    node_id = Column(GUID, ForeignKey('node.id'), nullable=False)
    parent_id = Column(GUID, nullable=True)
    update_date = Column(DateTime)

    def __repr__(self):
        return (f'Type - "{self.type}" '
                f'price - {self.price} '
                f'in period for {self.date} to {self.update_date}.')
