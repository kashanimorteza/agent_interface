"""Alembic environment: resolves the target Instance's URL and metadata
from Database's own runtime configuration rather than a hardcoded value.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from my_database import _orm  # noqa: F401 (registers every mapped table)
from my_database._config import load_runtime_configuration
from my_database._orm._base import Base
from my_database._session import _sqlite_url

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _resolve_url() -> str:
    runtime_config = load_runtime_configuration()
    default_key = runtime_config["default_instance"]
    instance_config = runtime_config["instances"][default_key]
    return _sqlite_url(str(instance_config["database"]))


def run_migrations_offline() -> None:
    context.configure(
        url=_resolve_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = _resolve_url()
    connectable = engine_from_config(configuration, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
