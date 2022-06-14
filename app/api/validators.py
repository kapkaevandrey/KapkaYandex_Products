from collections import defaultdict
from datetime import datetime
from http import HTTPStatus
from typing import Any, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD, ModelType
from app.crud import node_crud, node_history_crud
from app.schemas.node import NodeCreate
from app.models import ProductType, Node


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
                f'with {attr_name}={attr_value} not found!'
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


async def check_items_package_parent_id(
        session: AsyncSession, items: List[NodeCreate],
):
    package_items_parent_id = set()
    for item in items:
        if item.type == ProductType.category.value:
            package_items_parent_id.add(item.id)
        if (item.parent_id is None or
                item.parent_id in package_items_parent_id):
            continue
        parent = await try_get_object_by_attribute(
            node_crud, 'id', item.parent_id, session
        )
        if parent.type == ProductType.offer.value:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'{ProductType.offer.value} cannot be parent'
            )


async def check_category_unchanged(item: NodeCreate, item_obj: Node):
    if item.type != item_obj.type:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'You cannot change type of Node'
        )


async def check_date_valid(date: datetime, item_date: datetime):
    if date <= item_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'The update date cannot be less '
                   f'than the already existing date'
        )
