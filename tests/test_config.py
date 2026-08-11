from app.config import Settings


def test_settings_reads_database_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/news")

    settings = Settings()

    assert settings.database_url == "postgresql+asyncpg://user:pass@db:5432/news"


def test_settings_reads_secret_key_from_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "rahasia-dari-env")

    settings = Settings()

    assert settings.secret_key == "rahasia-dari-env"


def test_settings_has_separate_test_database_url(monkeypatch):
    monkeypatch.setenv("TEST_DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/news_test")

    settings = Settings()

    assert settings.test_database_url == "postgresql+asyncpg://user:pass@db:5432/news_test"