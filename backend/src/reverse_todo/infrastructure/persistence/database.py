from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from reverse_todo.config import get_settings
from reverse_todo.infrastructure.persistence.url import async_engine_options, to_async_database_url

settings = get_settings()
_async_url = to_async_database_url(str(settings.database_url))
engine = create_async_engine(
    _async_url,
    echo=settings.debug,
    **async_engine_options(_async_url),
)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@event.listens_for(engine.sync_engine, "connect")
def _sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    if engine.dialect.name != "sqlite":
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
