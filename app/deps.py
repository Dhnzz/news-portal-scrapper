from __future__ import annotations

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User
from app.security import SESSION_COOKIE_NAME, read_session_token


class LoginRequired(Exception):
    """Tamu mengakses rute yang butuh login; ditangani jadi redirect ke /login."""


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> User | None:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    payload = read_session_token(token, request.app.state.settings.secret_key)
    if payload is None or "uid" not in payload:
        return None
    result = await session.execute(select(User).where(User.id == payload["uid"]))
    return result.scalar_one_or_none()


async def require_login(user: User | None = Depends(get_current_user)) -> User:
    if user is None:
        raise LoginRequired()
    return user


async def require_admin(user: User = Depends(require_login)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Hanya admin yang dapat mengakses halaman ini.")
    return user