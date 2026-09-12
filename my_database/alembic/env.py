import os
from logging.config import fileConfig

from alembic import context
from my_database import _orm  # noqa: F401 - registers every mapped table
from my_database._base import Base, get_engine, get_runtime_config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _resolve_instance_key() -> str:
    return (
        os.environ.get("MY_DATABASE_ALEMBIC_INSTANCE")
        or get_runtime_config().default_instance
    )


def run_migrations_offline() -> None:
    instance = get_runtime_config().resolve(_resolve_instance_key())
    context.configure(
        url=str(get_engine(instance.key).url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = get_engine(_resolve_instance_key())
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
