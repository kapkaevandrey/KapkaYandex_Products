from app.models import NodeHistory
from app.schemas.node_history import NodeHistoryCreate, NodeHistoryUpdate
from app.crud.base import BaseCRUD

node_history_crud = BaseCRUD[
    NodeHistory, NodeHistoryCreate, NodeHistoryUpdate
](NodeHistory)
