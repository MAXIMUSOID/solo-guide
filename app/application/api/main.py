from fastapi import FastAPI
import uvicorn

from infra.repository.connect import _init_db
from application.api.messages.create_db import router as create_db
from application.api.messages.handlers import router as city
from application.api.messages.handlers import router_showplace as show_place

_init_db()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Сам Себе Гид",
        description="API для получения информации о достопримечательностях города"
    )
    app.include_router(create_db, prefix='/create_db')
    app.include_router(city, prefix='/city')
    app.include_router(show_place, prefix='/showplace')
    return app



    