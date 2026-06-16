import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import event, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from reverse_todo.config import get_settings
from reverse_todo.infrastructure.persistence.base import Base
from reverse_todo.infrastructure.persistence.models import *  # noqa: F403
from reverse_todo.infrastructure.persistence.url import async_engine_options, to_async_database_url

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return to_async_database_url(str(get_settings().database_url))


def run_migrations_offline() -> None:
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    url = get_url()
    configuration["sqlalchemy.url"] = url
    engine_options = async_engine_options(url)
    poolclass = engine_options.pop("poolclass", pool.NullPool)
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=poolclass,
        **engine_options,
    )

    @event.listens_for(connectable.sync_engine, "connect")
    def _sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
        if connectable.dialect.name != "sqlite":
            return
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
