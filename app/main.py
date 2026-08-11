from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.config import Settings
from app.db import close_db, init_db
from app.routers import health


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        init_db(app_settings)
        yield
        await close_db()

    app = FastAPI(title=app_settings.app_name, lifespan=lifespan)
    app.state.settings = app_settings
    app.include_router(health.router)
    return app


app = create_app()