from app.models import NodeBase

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from fastapi_users_db_sqlalchemy import GUID


class NodeHistory(NodeBase):
    id = Column(Integer, primary_key=True)
    node_id = Column(GUID, ForeignKey('node.id'), nullable=False)
    update_date = Column(DateTime)

    def __repr__(self):
        return (f'Type - "{self.type}" '
                f'price - {self.price} '
                f'in period for {self.date} to {self.update_date}.')
    # TODO constraint date < update_date
