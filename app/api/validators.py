from collections import defaultdict
from datetime import datetime
from http import HTTPStatus
from typing import Any, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD, ModelType
from app.crud import node_crud
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


def check_items_package_id(
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


def check_category_unchanged(item: NodeCreate, item_obj: Node):
    if item.type != item_obj.type:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='You cannot change type of Node'
        )


def check_price_category_unchanged(item: NodeCreate, item_obj: Node):
    if (item_obj.type == ProductType.category.value and
            item.price != item_obj.price):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Price of category calculate automatically'
        )


def check_date_valid(date: datetime, item_date: datetime) -> None:
    if date <= item_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The update date cannot be less '
                   'than the already existing date'
        )


def date_lees_then_now(date: datetime) -> None:
    if date > datetime.now(tz=date.tzinfo):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The date cannot be greater '
                   'than the current date'
        )


def valid_time_period(
        start_time: datetime, end_time: datetime
) -> None:
    if start_time >= end_time:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='The start date cannot be greater or equal '
                   'than the end date'
        )
