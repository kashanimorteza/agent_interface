"""Alembic environment: migrates the storage of a configured Instance to match the Model's Entities.

The Instance comes from the Database Configuration (the default Instance unless `-x instance=<key>` is given).
"""

from logging.config import fileConfig

from alembic import context

from database import data, structure

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = structure.metadata


def run_migrations_online() -> None:
    """Run migrations against the storage of the requested Instance."""
    instance = context.get_x_argument(as_dictionary=True).get("instance")
    with data.resolve(instance).sql_engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, render_as_batch=True
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError(
        "Offline migration is not supported; migrate a configured Instance directly."
    )
run_migrations_online()
