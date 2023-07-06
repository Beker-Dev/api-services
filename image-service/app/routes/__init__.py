from fastapi import APIRouter
from . import (
    image,
)


api_router = APIRouter(prefix='/api')
api_router.include_router(image.router)
