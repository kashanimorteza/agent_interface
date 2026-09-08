"""How a recorded structural change reaches the selected Instance.

The structure to compare against is the one derived from the shared
definitions, and the connection is the layer's own — resolved from its settings
rather than written into the history's configuration.
"""

from __future__ import annotations

import os

from alembic import context

from my_database.data_logic.mapping import metadata
from my_database.storage_adapter import Connections

target_metadata = metadata

_connections = Connections()
_connection = _connections.for_instance(os.environ.get("MY_DATABASE_INSTANCE") or None)


def run_migrations_offline() -> None:
    context.configure(
        url=str(_connection.engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        render_as_batch=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with _connection.engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
