"""Alembic environment: resolves the target Database Instance and metadata from Database's
own runtime configuration rather than a hardcoded URL."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from alembic import context
from sqlalchemy import engine_from_config, pool

from database.mapping import Base
from database.runtime_config import load_runtime_config

config = context.config

_db_url = config.get_main_option("sqlalchemy.url")
if not _db_url:
    _runtime_config = load_runtime_config()
    _instance_name = config.get_main_option("database_instance", None)
    _instance = _runtime_config.resolve_instance(_instance_name)
    _engine_profile = _runtime_config.engines[_instance.engine]
    _db_path = _runtime_config.storage_path(_instance)
    _db_url = f"{_engine_profile.url_scheme}:///{_db_path}"
    config.set_main_option("sqlalchemy.url", _db_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=_db_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
