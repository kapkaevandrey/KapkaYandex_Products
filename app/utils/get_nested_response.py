from collections import deque

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import node_crud
from app.models.node import Node
from app.schemas.node import NodeRead, NodeFullRead


async def create_nested_response(
        session: AsyncSession,
        node: Node,
) -> NodeRead:
    node_item = NodeRead.from_orm(node)
    node_response = NodeFullRead(**node_item.dict(), children=None)
    node_response.date = node_response.date.isoformat(
        timespec='milliseconds'
    ) + 'Z'
    node_response.parent_id = node.parent_id
    children_response_deque = deque()
    children_response_deque.append(node_response)
    while children_response_deque:
        current_node = children_response_deque.popleft()
        children = await node_crud.get_by_attributes(
            {'parent_id': current_node.id}, session=session, many=True,
            order_by='date', desc=True
        )
        if children:
            current_node.children = []
            for child in children:
                new_node = NodeFullRead(
                    **NodeRead.from_orm(child).dict(), children=None
                )
                new_node.date = new_node.date.isoformat(
                    timespec='milliseconds'
                ) + 'Z'
                new_node.parent_id = child.parent_id
                current_node.children.append(new_node)
                children_response_deque.append(new_node)
    return node_response
