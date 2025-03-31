from fastapi import FastAPI
import uvicorn

import flet as ft
import flet.fastapi as flet_fastapi

from application.front import main_window as flet_window
from infra.repository.connect import _init_db
from application.api.messages.create_db import router as create_db
from application.api.messages.handlers import router as city
from application.api.messages.handlers import router_showplace as show_place
from application.api.messages.handlers import router_user as user
from application.api.messages.handlers import router_visit as visit


_init_db()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Сам Себе Гид",
        description="API для получения информации о достопримечательностях города",
        lifespan=flet_window.lifespan
    )
    app.include_router(create_db, prefix='/create_db')
    app.include_router(city, prefix='/city')
    app.include_router(show_place, prefix='/showplace')
    app.include_router(user, prefix='/user')
    app.include_router(visit, prefix='/visit')

    app.mount("/flet-app", flet_fastapi.app(flet_window.main_window))
    return app



    