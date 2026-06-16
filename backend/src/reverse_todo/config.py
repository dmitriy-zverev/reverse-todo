from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Reverse To-Do"
    debug: bool = False
    secret_key: str = Field(min_length=32)
    database_url: str = "sqlite+aiosqlite:///./reverse_todo.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    cookie_name: str = "reverse_todo_session"
    cookie_secure: bool = False
    cookie_samesite: Literal["lax", "strict", "none"] = "lax"
    access_token_expire_minutes: int = 60 * 24 * 7
    classifier_backend: Literal["rules", "llm"] = "rules"
    entry_text_max_length: int = 2000
    default_timezone: str = "UTC"
    rate_limit_entries: str = "60/minute"
    rate_limit_auth: str = "10/minute"
    telegram_bot_token: str | None = None
    telegram_webhook_secret: str | None = None


SettingsDep = Annotated[Settings, ...]


@lru_cache
def get_settings() -> Settings:
    return Settings()
