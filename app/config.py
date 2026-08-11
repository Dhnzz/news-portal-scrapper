from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "news-portal-scrapper"
    database_url: str = "postgresql+asyncpg://news:news@localhost:5432/news"
    test_database_url: str = "postgresql+asyncpg://news:news@localhost:5433/news_test"
    secret_key: str = Field(description="Secret aplikasi; wajib dari environment")