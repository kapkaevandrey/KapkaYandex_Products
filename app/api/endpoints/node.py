from datetime import datetime
from typing import List, Optional
from http import HTTPStatus


from fastapi import APIRouter, Depends, Query, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.api.validators import (
    check_items_package_id, check_category_unchanged,
    check_items_package_parent_id, check_date_valid,
    check_price_category_unchanged, date_lees_then_now,
    try_get_object_by_attribute, valid_time_period
)
from app.core.db import get_async_session
from app.core.config import settings
from app.crud import node_crud
from app.schemas.node import NodeListCreate, NodeList
from app.schemas.node_history import NodeHistoryListRead, NodeHistoryRead
from app.utils.update_create_process import (
    update_or_create_items_package, category_price_update
)
from app.utils.get_nested_response import create_nested_response
from app.utils.get_sales_statistics import (
    get_offer_sales, get_node_update_statistic
)


router = APIRouter()


@router.post(
    '/imports',
    status_code=HTTPStatus.OK
)
async def import_products_or_categories(
        items_data: NodeListCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can import data about categories or products___
    """
    check_items_package_id(items_data.items)
    await check_items_package_parent_id(session, items_data.items)
    for item in items_data.items:
        item_obj = await node_crud.get(item.id, session)
        if item_obj is not None:
            check_category_unchanged(item, item_obj)
            check_date_valid(items_data.date, item_obj.date)
            check_price_category_unchanged(item, item_obj)
    await update_or_create_items_package(session, items_data)


@router.get(
    '/nodes/{id}',
)
async def get_info_about_node(
        node_id: UUID4 = Path(alias='id'),
        session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can see information about product or category.___
    """
    node = await try_get_object_by_attribute(
        node_crud, attr_name='id', attr_value=node_id, session=session
    )
    node = await create_nested_response(session, node)
    return node


@router.delete(
    '/delete/{id}',
    status_code=HTTPStatus.OK
)
async def import_products_or_categories(
    node_id: UUID4 = Path(alias='id'),
    session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can delete info about product or category___
    """
    node = await try_get_object_by_attribute(
        node_crud, attr_name='id', attr_value=node_id, session=session
    )
    node_removed = await node_crud.remove(node, session)
    if node_removed.parent_id is not None:
        category_objects = await category_price_update(
            session, node_removed.parent_id, datetime.now()
        )
        session.add_all(tuple(category_objects))
        await session.commit()
        [await session.refresh(single_obj) for single_obj in category_objects]


@router.get(
    '/sales',
    response_model=NodeList
)
async def get_product_price_update_last_date(
     date: datetime = Query(),
     session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can see information about product or category.___
    """
    start_time = date - settings.statistic_time_period
    offers = await get_offer_sales(session, start_time)
    return NodeList(items=offers)


@router.get(
    '/node/{id}/statistics',
    response_model=NodeList
)
async def get_product_price_update_last_date(
        node_id: UUID4 = Path(alias='id'),
        date_start: Optional[datetime] = Query(None, alias='dateStart'),
        date_end: Optional[datetime] = Query(None, alias='dateEnd'),
        session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can see price statistics for this product or
        category.___
    """
    node = await try_get_object_by_attribute(
        node_crud, attr_name='id', attr_value=node_id, session=session
    )
    if date_start is not None:
        date_lees_then_now(date_start)
    if date_end is not None:
        date_lees_then_now(date_end)
    if date_start is not None and date_end is not None:
        valid_time_period(date_start, date_end)
    node_statistic = await get_node_update_statistic(
        session, node, date_start, date_end
    )
    return NodeHistoryListRead(
        items=[NodeHistoryRead(
            price=node.price, date=node.date, name=node.name,
            type=node.type, parentId=node.parent_id,
            id=node.node_id
        ) for node in node_statistic]
    )



