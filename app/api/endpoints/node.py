from datetime import datetime
from typing import List, Optional


from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

from app.schemas.node import NodeListCreate, NodeRead
from app.core.db import get_async_session
from app.api.validators import check_items_package_id, try_create_or_update_node

router = APIRouter()


@router.post(
    '/imports',
    # response_model=List[NodeRead],
)
async def import_products_or_categories(
        items_data: NodeListCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can import data about categories or products___
    """
    # валидация данных
    # валидация формата объект
    await check_items_package_id(items_data.items)
    await try_create_or_update_node(
        session, items_data.date, *items_data.items
    )
    return


@router.get(
    '/nodes/{node_id}',
)
async def get_info_about_node(
        node_id: UUID4,
        session: AsyncSession = Depends(get_async_session)
):
    """
        ___You can see information about product or category.___
    """
    pass


@router.delete(
    '/delete/{id}'
)
async def import_products_or_categories(
    node_id: UUID4
):
    """
        ___You can delete info about product or category___
    """
    pass


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


