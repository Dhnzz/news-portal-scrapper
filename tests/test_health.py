import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.db import get_session


class FakeSession:
    def __init__(self, *, ok: bool = True):
        self._ok = ok

    async def execute(self, *args, **kwargs):
        if not self._ok:
            raise OSError("connection to server lost")
        return None

    async def close(self):
        return None


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def override_db(client):
    def _override(ok: bool):
        async def override_get_session():
            yield FakeSession(ok=ok)

        client.app.dependency_overrides[get_session] = override_get_session

    return _override


def test_health_returns_ok_when_db_is_up(client, override_db):
    override_db(ok=True)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}


def test_health_returns_503_when_db_is_down(client, override_db):
    override_db(ok=False)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "down"}