from datetime import datetime
from typing import List, Optional


from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

router = APIRouter()


@router.get(
    '/nodes/{node_id}'
)
async def get_info_about_node(
     node_id: UUID4
):
    """
        ___You can see information about product or category.___
    """
    pass


@router.post(
    '/imports'
)
async def import_products_or_categories():
    """
        ___You can import data about categories or products___
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


