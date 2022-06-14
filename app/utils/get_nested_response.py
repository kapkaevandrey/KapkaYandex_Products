from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import node_crud
from app.models.node import Node
from app.schemas.node import NodeRead, NodeFullRead


async def create_nested_response(
        session: AsyncSession,
        node: Node,
) -> NodeRead:
    node_item = NodeRead.from_orm(node)
    return node_item
