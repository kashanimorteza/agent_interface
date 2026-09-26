"""Migration environment: compares and migrates the default Database Instance against the Entity metadata."""

from logging.config import fileConfig

from alembic import context

from my_database.configuration import Configuration
from my_database.mapping import Mapping
from my_database.schema import metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

default = Mapping(Configuration.load()).resolve(None)
# the default Database Instance is validated when the configuration loads
assert default is not None
engine = default.engine
options = {"target_metadata": metadata(), "compare_type": True, "render_as_batch": True}


def run_migrations_offline() -> None:
    """Emit migration statements as text without connecting to the storage."""
    context.configure(
        url=engine.url.render_as_string(hide_password=False),
        literal_binds=True,
        **options,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the storage of the default Database Instance."""
    with engine.connect() as connection:
        context.configure(connection=connection, **options)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
