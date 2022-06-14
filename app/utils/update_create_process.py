from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import node_crud, node_history_crud
from app.models import Node, NodeHistory
from app.schemas.node import NodeListCreate


async def update_or_create_items_package(
        session: AsyncSession,
        items_data: NodeListCreate,
):
    date = items_data.date
    objects = []
    history_objects = []
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
        objects.append(node_obj)
    session.add_all(tuple(objects))
    await session.commit()
    [await session.refresh(single_obj) for single_obj in objects]
