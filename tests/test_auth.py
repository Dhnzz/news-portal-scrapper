async def test_guest_redirected_to_login_on_home(client):
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


async def test_guest_redirected_to_login_on_admin(client):
    response = await client.get("/admin", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


async def test_login_success_sets_session_cookie_and_accesses_home(client, make_user, login):
    await make_user("admin", "admin123", role="admin")

    response = await login(client, "admin", "admin123")
    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert "news_session" in client.cookies

    home = await client.get("/")
    assert home.status_code == 200
    assert "admin" in home.text


async def test_login_failure_wrong_password(client, make_user, login):
    await make_user("admin", "admin123")

    response = await login(client, "admin", "salah")
    assert response.status_code == 401
    assert "news_session" not in client.cookies


async def test_login_failure_unknown_user(client, login):
    response = await login(client, "tidak-ada", "admin123")
    assert response.status_code == 401
    assert "news_session" not in client.cookies


async def test_logout_clears_session(client, make_user, login):
    await make_user("admin", "admin123")
    await login(client, "admin", "admin123")
    assert "news_session" in client.cookies

    logout = await client.post("/logout", follow_redirects=False)
    assert logout.status_code == 303
    assert logout.headers["location"] == "/login"
    assert "news_session" not in client.cookies

    home = await client.get("/", follow_redirects=False)
    assert home.status_code == 303


async def test_anonymous_logout_redirects_to_login(client):
    response = await client.post("/logout", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


async def test_login_page_redirects_when_already_logged_in(client, make_user, login):
    await make_user("admin", "admin123")
    await login(client, "admin", "admin123")

    response = await client.get("/login", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/"


async def test_tampered_session_treated_as_guest(client, make_user):
    await make_user("admin", "admin123")
    client.cookies.set("news_session", "palsu.palsu")
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/login"