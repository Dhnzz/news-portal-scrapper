import pytest

from app.security import verify_password


async def _login(client, username: str, password: str):
    return await client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


async def test_member_cannot_access_admin_page(client, make_user):
    await make_user("nina", "rahasia123", role="anggota")
    await _login(client, "nina", "rahasia123")

    response = await client.get("/admin", follow_redirects=False)
    assert response.status_code == 403


async def test_admin_page_lists_users(client, make_user):
    await make_user("boss", "admin123", role="admin")
    await make_user("budi", "rahasia123", role="anggota")
    await _login(client, "boss", "admin123")

    response = await client.get("/admin")
    assert response.status_code == 200
    assert "boss" in response.text
    assert "budi" in response.text


async def test_admin_creates_member(client, db, make_user):
    await make_user("boss", "admin123", role="admin")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "budi", "password": "rahasia123", "role": "anggota"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/admin"

    login = await _login(client, "budi", "rahasia123")
    assert login.status_code == 303
    assert "news_session" in client.cookies


async def test_admin_creates_another_admin(client, db, make_user):
    await make_user("boss", "admin123", role="admin")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "co-boss", "password": "admin456", "role": "admin"},
        follow_redirects=False,
    )
    assert response.status_code == 303

    await client.post("/logout", follow_redirects=False)
    login = await _login(client, "co-boss", "admin456")
    assert login.status_code == 303
    admin_page = await client.get("/admin")
    assert admin_page.status_code == 200


async def test_created_user_password_stored_as_hash(client, db, make_user):
    await make_user("boss", "admin123", role="admin")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "budi", "password": "rahasia123", "role": "anggota"},
        follow_redirects=False,
    )
    assert response.status_code == 303

    async with db() as session:
        from app.users import fetch_user_by_username

        user = await fetch_user_by_username(session, "budi")
        assert user is not None
        assert user.password_hash != "rahasia123"
        assert user.password_hash.startswith("pbkdf2_sha256$")
        assert verify_password("rahasia123", user.password_hash)


async def test_duplicate_username_rejected(client, make_user):
    await make_user("boss", "admin123", role="admin")
    await make_user("budi", "rahasia123")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "budi", "password": "rahasia123", "role": "anggota"},
        follow_redirects=False,
    )
    assert response.status_code == 400
    assert "sudah dipakai" in response.text


async def test_short_password_rejected(client, make_user):
    await make_user("boss", "admin123", role="admin")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "cecep", "password": "pendek", "role": "anggota"},
        follow_redirects=False,
    )
    assert response.status_code == 400


async def test_invalid_role_rejected(client, make_user):
    await make_user("boss", "admin123", role="admin")
    await _login(client, "boss", "admin123")

    response = await client.post(
        "/admin/users",
        data={"username": "cecep", "password": "rahasia123", "role": "superadmin"},
        follow_redirects=False,
    )
    assert response.status_code == 400


async def test_member_cannot_create_user(client, make_user):
    await make_user("nina", "rahasia123", role="anggota")
    await _login(client, "nina", "rahasia123")

    response = await client.post(
        "/admin/users",
        data={"username": "x", "password": "rahasia123", "role": "anggota"},
        follow_redirects=False,
    )
    assert response.status_code == 403