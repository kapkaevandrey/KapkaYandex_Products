from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, or_, between
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Node, NodeHistory, ProductType


async def get_offer_sales(
        session: AsyncSession,
        date_start: datetime
) -> List[Node]:
    all_update_offer_data = await session.execute(
        select(Node).where(
            Node.type == ProductType.category.offer,
            Node.date >= date_start
        )
    )
    return await get_only_offer_price_update(
        session, date_start, all_update_offer_data.scalars().all()
    )


async def get_only_offer_price_update(
        session: AsyncSession,
        date_start: datetime,
        nodes: List[Node]
) -> List[Node]:
    price_changed_nodes = []
    for node in nodes:
        history_node_price = await session.execute(
            select(NodeHistory.price).where(
                and_(
                    NodeHistory.node_id == node.id,
                    or_(
                        NodeHistory.date >= date_start,
                        NodeHistory.update_date > date_start
                    )
                )
            )
        )
        if len(set(history_node_price)) > 1:
            price_changed_nodes.append(node)
    return price_changed_nodes


async def get_node_update_statistic(
        session: AsyncSession,
        node: Node,
        date_start: Optional[datetime] = None,
        date_end: Optional[datetime] = None
):
    select_stmt = select(NodeHistory)
    if date_start is not None and date_end is not None:
        select_stmt = select_stmt.where(
            NodeHistory.node_id == node.id,
            between(NodeHistory.update_date, date_start, date_end),
            between(NodeHistory.date, date_start, date_end)
        )
    elif date_start is not None:
        select_stmt = select_stmt.where(
            NodeHistory.node_id == node.id,
            NodeHistory.update_date >= date_start
        )
    elif date_end is not None:
        select_stmt = select_stmt.where(
            NodeHistory.node_id == node.id,
            NodeHistory.date <= date_end
        )
    else:
        select_stmt = select_stmt.where(
            NodeHistory.node_id == node.id,
        )
    data_history = await session.execute(
        select_stmt.order_by(NodeHistory.date)
    )
    return data_history.scalars().all()
