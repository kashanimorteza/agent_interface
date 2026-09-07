"""Alembic environment: migrates the Instance resolved through the Database
settings boundary (DATABASE__DEFAULT_INSTANCE, or ``-x instance=<key>``)."""

from alembic import context

from my_database.errors import UnknownInstanceError
from my_database.storage_adapter import load_settings, make_engine

settings = load_settings()
key = (context.get_x_argument(as_dictionary=True).get("instance") or settings.default).strip().lower()
if key not in settings.instances:
    raise UnknownInstanceError(f"Instance {key!r} is not configured; configured Instances: {', '.join(settings.instances)}")
engine = make_engine(settings.instances[key])

with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=None, transaction_per_migration=True)
    with context.begin_transaction():
        context.run_migrations()
engine.dispose()
