from app.models import Node
from app.schemas.node import NodeCreate, NodeUpdate
from app.crud.base import BaseCRUD

node_crud = BaseCRUD[Node, NodeCreate, NodeUpdate](Node)
