from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.deps import get_current_user, require_login
from app.models import User
from app.security import (
    SESSION_COOKIE_NAME,
    SESSION_TTL_SECONDS,
    create_session_token,
    verify_password,
)
from app.templating import templates
from app.users import fetch_user_by_username

router = APIRouter()


@router.get("/login")
async def login_page(request: Request, user: User | None = Depends(get_current_user)) -> Response:
    if user is not None:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
) -> Response:
    user = await fetch_user_by_username(session, username.strip())
    if user is None or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request, "login.html", {"error": "Username atau password salah."}, status_code=401
        )
    token = create_session_token(user.id, request.app.state.settings.secret_key)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@router.post("/logout")
async def logout(request: Request, user: User = Depends(require_login)) -> Response:
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return response


@router.get("/")
async def home(request: Request, user: User = Depends(require_login)) -> Response:
    return templates.TemplateResponse(request, "home.html", {"user": user})