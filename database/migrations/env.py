"""Alembic environment wired to the Storage Adapter mappings and runtime settings."""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context

from ta_database.settings import get_settings
from ta_database.storage_adapter.engine import get_engine
from ta_database.storage_adapter.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The URL comes only from runtime configuration; alembic.ini carries none.
config.set_main_option("sqlalchemy.url", get_settings().database_url.replace("%", "%%"))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = get_engine(get_settings().database_url)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
