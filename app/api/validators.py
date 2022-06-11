from collections import defaultdict
from datetime import datetime
from http import HTTPStatus
from typing import Any, List, Union


from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD, ModelType
from app.crud import node_crud, node_history_crud
from app.schemas.node import NodeCreate


async def check_unique_attribute(
        crud_obj: BaseCRUD,
        attr_name: str,
        attr_value: Any,
        session: AsyncSession
) -> None:
    result = await crud_obj.get_by_attributes(
        {attr_name: attr_value}, session
    )
    if result is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Field {attr_name} must be unique'
        )


async def try_get_object_by_attribute(
        crud_obj: BaseCRUD,
        attr_name: str,
        attr_value: Any,
        session: AsyncSession
) -> ModelType:
    result = await crud_obj.get_by_attributes(
        {attr_name: attr_value}, session
    )
    if result is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(
                f'{crud_obj.model.__name__} '
                f'с значением {attr_name}={attr_value} не найден!'
            )
        )
    return result


async def check_items_package_id(
        items: List[NodeCreate],
):
    uniq_id_counter = defaultdict(list)
    for node in items:
        uniq_id_counter[node.id].append(node)
        if len(uniq_id_counter[node.id]) > 1:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    f'Item name={node.name} have equal id={node.id} '
                    f'with item name={uniq_id_counter[node.id][0].name} '
                    f'id={uniq_id_counter[node.id][0].id} '
                    f'please check package'
                )
            )


async def try_create_or_update_node(
        session: AsyncSession,
        update_date: datetime,
        *items: List[NodeCreate]
):
    nodes = [None] * len(items)
    history_nodes = [None] * len(items)
    for item in items:
        node = await node_crud.get_by_attributes({'id': item.id}, session)
        if node is None:
            node = await node_crud.create(
                data=item, session=session, commit=False, date=update_date
            )
            # Save logic
        else:
            # Update Logic
            pass




