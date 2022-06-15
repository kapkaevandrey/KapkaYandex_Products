from collections import deque
from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import node_crud, node_history_crud
from app.models import Node, ProductType
from app.schemas.node import NodeListCreate
from app.schemas.node_history import NodeHistoryCreate


async def update_or_create_items_package(
        session: AsyncSession,
        items_data: NodeListCreate,
):
    date = items_data.date
    category_objects, offer_objects = [], []
    history_objects = []
    need_update_category_id = set()
    for item in items_data.items:
        node_obj = await node_crud.get(pk=item.id, session=session)
        if node_obj is None:
            node_obj = await node_crud.create(
                data=item, session=session, commit=False, date=date
            )
        else:
            node_obj = await node_crud.update(
                node_obj, item, session, commit=False, date=date
            )
        history_objects += await create_history_object(
            session, node_obj, date,
        )
        offer_objects.append(node_obj)
        if (node_obj.type == ProductType.offer.value and
                node_obj.parent_id is not None):
            need_update_category_id.add(node_obj.parent_id)
    session.add_all(tuple(offer_objects) + tuple(history_objects))
    await session.commit()
    [await session.refresh(single_obj) for single_obj in offer_objects]
    for unique_id in need_update_category_id:
        category_objects += await category_price_update(
            session, unique_id, date,
        )
    session.add_all(tuple(category_objects))
    await session.commit()
    [await session.refresh(single_obj) for single_obj in category_objects]


async def create_history_object(
        session: AsyncSession,
        node_obj: Node,
        date: datetime
):
    updated_objects = []
    history_node = await node_history_crud.get_by_attributes(
        {'node_id': node_obj.id}, order_by='date', session=session
    )
    if history_node is not None:
        history_node.update_date = date
        updated_objects.append(history_node)
    new_history_node = await node_history_crud.create(
        NodeHistoryCreate(
            name=node_obj.name, type=node_obj.type,
            parentId=node_obj.parent_id,
            price=node_obj.price, date=date, id=node_obj.id
        ), session, commit=False
    )
    updated_objects.append(new_history_node)
    return updated_objects


async def category_price_update(
        session: AsyncSession, category_id: UUID, date: datetime,
) -> List[Node]:
    async def update_price(
            parent_id, summary, counter, id_checked,
            history=None
    ):
        current_deque = deque()
        current_node = await node_crud.get(pk=parent_id, session=session)
        current_deque.append(parent_id)
        while current_deque:
            current_id = current_deque.popleft()
            data_offer = await session.execute(
                select(
                    func.sum(Node.price), func.count(Node.id)
                ).where(
                    Node.parent_id == current_id,
                    Node.type == ProductType.offer.value
                )
            )
            amount, obj_count = data_offer.first()
            summary = summary if amount is None else summary + amount
            counter = counter if obj_count is None else counter + obj_count
            data_category = await session.execute(
                select(
                    Node
                ).where(
                    Node.parent_id == current_id,
                    Node.type == ProductType.category.value
                )
            )
            child_categories = data_category.scalars().all()
            if child_categories:
                [current_deque.append(category.id)
                 for category in child_categories if
                 category.id not in id_checked]
        current_node.price = int(summary / counter) if counter > 0 else None
        updated_categories.append(current_node)
        history += await create_history_object(session, current_node, date)
        id_checked.add(current_node.id)
        if current_node.parent_id is not None:
            await update_price(
                current_node.parent_id, summary, counter, id_checked,
                history
            )
    updated_categories = []
    history_categories = []
    checked_id = set()
    total, numbers = 0, 0
    await update_price(
        parent_id=category_id,
        summary=total, counter=numbers, id_checked=checked_id,
        history=history_categories
    )
    return updated_categories + history_categories
