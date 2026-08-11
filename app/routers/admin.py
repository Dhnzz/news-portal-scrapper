from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.deps import require_admin
from app.models import User
from app.templating import templates
from app.users import create_user

router = APIRouter()


async def _admin_response(
    request: Request,
    session: AsyncSession,
    *,
    user: User,
    error: str | None,
    status_code: int = 200,
) -> Response:
    result = await session.execute(select(User).order_by(User.id))
    users = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "admin.html",
        {"user": user, "users": users, "error": error},
        status_code=status_code,
    )


@router.get("/admin")
async def admin_page(
    request: Request,
    user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> Response:
    return await _admin_response(request, session, user=user, error=None)


@router.post("/admin/users")
async def admin_create_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("anggota"),
    user: User = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> Response:
    try:
        await create_user(session, username, password, role)
        await session.commit()
    except (ValueError, IntegrityError) as exc:
        await session.rollback()
        if isinstance(exc, IntegrityError):
            error = "Username sudah dipakai."
        else:
            error = str(exc)
        return await _admin_response(request, session, user=user, error=error, status_code=400)
    return RedirectResponse("/admin", status_code=303)