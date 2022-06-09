from fastapi import APIRouter
from app.api.endpoints import node_router


main_router = APIRouter()
main_router.include_router(
    node_router,
    tags=['Category and Products']
)
# main_router.include_router(user_router)