"""Alembic environment: migrates the configured default Instance, or the Instance named with ``-x instance=<name>``."""

import model.interface  # noqa: F401  (registers every Entity's storage structure)
from alembic import context
from sqlmodel import SQLModel

from database import data

target_metadata = SQLModel.metadata


def run_migrations() -> None:
    if context.is_offline_mode():
        raise RuntimeError("Offline migrations are not supported")
    instance = context.get_x_argument(as_dictionary=True).get("instance")
    engine = data.resolve(instance).engine.sql
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations()
