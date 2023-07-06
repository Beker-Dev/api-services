from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import api_router
# from app.database import Base, engine


def init_database():
    # Base.metadata.create_all(bind=engine)
    pass


def get_app():
    _app = FastAPI(title=settings.PROJECT_TITLE, root_path=settings.ROOT_PATH)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    _app.include_router(api_router)
    init_database()
    return _app


app = get_app()
