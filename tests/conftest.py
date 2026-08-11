import os

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["PASSWORD_HASH_ITERATIONS"] = "10000"

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401 — daftarkan model ke Base.metadata
from app.db import Base, get_session
from app.main import create_app
from app.users import create_user


@pytest_asyncio.fixture
async def db():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield maker
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db):
    async def override_get_session():
        async with db() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client


@pytest_asyncio.fixture
async def make_user(db):
    async def _make(username: str, password: str, role: str = "anggota"):
        async with db() as session:
            user = await create_user(session, username, password, role)
            await session.commit()
            return user

    return _make