"""Migration environment of the Database package.

Internal tooling: it changes the physical storage structure of the selected
Instance through the Storage Adapter's resolved technology. The Instance is
selected with the ``TRADING_ASSISTANT_DATABASE_INSTANCE`` environment
variable and defaults to the default Instance.
"""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context

from my_database.adapter.connection import StorageAdapter
from my_database.logic.mapping import StorageMapping
from my_database.runtime import INSTANCE_ENV, resolve_settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = resolve_settings()
adapter = StorageAdapter(settings)
instance_key = os.environ.get(INSTANCE_ENV) or settings.default_instance
target_metadata = StorageMapping().metadata


def run_migrations_offline() -> None:
    context.configure(
        url=adapter.url(instance_key),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with adapter.engine(instance_key).connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
