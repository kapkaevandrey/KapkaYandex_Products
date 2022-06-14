from datetime import datetime
from typing import List, Optional
from http import HTTPStatus


from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.schemas.node import NodeListCreate, NodeRead
from app.core.db import get_async_session
from app.crud import node_crud
from app.api.validators import (
    check_items_package_id, check_category_unchanged,
    check_items_package_parent_id, check_date_valid,
    check_price_category_unchanged,
    try_get_object_by_attribute
)
from app.utils.update_create_process import (
    update_or_create_items_package, category_price_update
)
from app.utils.get_nested_response import create_nested_response


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
    '/nodes/{node_id}',
    response_model=NodeRead,
)
async def get_info_about_node(
        node_id: UUID4,
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
    node_id: UUID4,
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
    '/sales'
)
async def get_product_price_update_last_date(
     date: datetime
):
    """
        ___You can see information about product or category.___
    """
    pass


@router.get(
    '/node/{node_id}/statistics'
)
async def get_product_price_update_last_date(
        node_id: UUID4,
        dateStart: Optional[datetime], # прописать alias
        dateEnd: Optional[datetime]
):
    """
        ___You can see price statistics for this product or
        category.___
    """
    pass


