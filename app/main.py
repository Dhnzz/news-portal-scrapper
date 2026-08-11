from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

from app.config import Settings
from app.db import close_db, init_db
from app.deps import LoginRequired
from app.routers import admin, auth, health


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        init_db(app_settings)
        yield
        await close_db()

    app = FastAPI(title=app_settings.app_name, lifespan=lifespan)
    app.state.settings = app_settings

    @app.exception_handler(LoginRequired)
    async def _login_required_handler(request: Request, exc: LoginRequired) -> RedirectResponse:
        return RedirectResponse("/login", status_code=303)

    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(admin.router)
    return app


app = create_app()