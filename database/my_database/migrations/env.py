"""Migration environment of the Database package.

Internal tooling: it changes the physical storage structure of the selected
Instance through the Storage Adapter's resolved technology. Pass ``-x
instance=<key>`` to act on a declared Instance other than the default, and
``-x config=<path>`` to run against an alternative layer configuration.
"""

from __future__ import annotations

from logging.config import fileConfig
from pathlib import Path

from alembic import context

from my_database.adapter.connection import StorageAdapter
from my_database.config import resolve_settings
from my_database.logic.mapping import StorageMapping

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

arguments = context.get_x_argument(as_dictionary=True)
settings = resolve_settings(Path(arguments["config"]) if arguments.get("config") else None)
adapter = StorageAdapter(settings)
instance_key = adapter.instances.resolve_key(arguments.get("instance"))
target_metadata = StorageMapping(engine=settings.instances[instance_key].engine).metadata


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
