from sqlalchemy.pool import NullPool


def to_async_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


def async_engine_options(url: str) -> dict:
    if "sqlite" not in url:
        return {}
    return {
        "connect_args": {"check_same_thread": False},
        "poolclass": NullPool,
    }
