from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from database.config import sqlite_url
from database.mapping import METADATA

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Database's mapped metadata, derived from Model's published persistence
# contracts (see database.mapping) — the single source autogenerate compares
# against.
target_metadata = METADATA

# Resolve the URL dynamically from Database's own runtime storage
# configuration and the selected Instance (an ``-x instance=<key>`` option),
# never a static alembic.ini value.
instance = context.get_x_argument(as_dictionary=True).get("instance")
config.set_main_option("sqlalchemy.url", sqlite_url(instance))


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

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
