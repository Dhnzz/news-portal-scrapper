from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import VALID_ROLES, User
from app.security import hash_password

MIN_PASSWORD_LENGTH = 8


async def fetch_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    username: str,
    password: str,
    role: str = "anggota",
) -> User:
    username = username.strip()
    if not username:
        raise ValueError("Username tidak boleh kosong.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password minimal {MIN_PASSWORD_LENGTH} karakter.")
    if role not in VALID_ROLES:
        raise ValueError(f"Role harus salah satu dari {', '.join(VALID_ROLES)}.")
    if await fetch_user_by_username(session, username) is not None:
        raise ValueError(f"Username '{username}' sudah dipakai.")
    user = User(username=username, password_hash=hash_password(password), role=role)
    session.add(user)
    return user