from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description
)
app.include_router(main_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content=jsonable_encoder(
            dict(detail=exc.errors(), body=exc.body)
        )
    )


@app.on_event('startup')
async def startup():
    await create_first_superuser()
