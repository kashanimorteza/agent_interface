"""Engine binding: one SQLAlchemy Engine per Instance, created from its internal
settings. Only the SQLite Engine is implemented in this package version."""

from __future__ import annotations

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, URL

from ..errors import ConfigurationError, UnsupportedEngineError
from .settings import InstanceSettings, resolve_path

SUPPORTED_ENGINES = ("sqlite",)


def make_engine(instance: InstanceSettings) -> Engine:
    """An Engine for the Instance. Creating it opens no connection; the database
    file (and its directory) is created on the first connection."""
    if instance.engine not in SUPPORTED_ENGINES:
        raise UnsupportedEngineError(
            f"Instance {instance.key!r} binds Engine {instance.engine!r}; this package implements {', '.join(SUPPORTED_ENGINES)}"
        )
    if not instance.file:
        raise ConfigurationError(f"Instance {instance.key!r} has no database file configured")
    path = resolve_path(instance.file)
    engine = create_engine(URL.create("sqlite", database=str(path)), connect_args={"check_same_thread": False})

    @event.listens_for(engine, "do_connect")
    def _prepare(dialect, conn_rec, cargs, cparams):  # noqa: ANN001
        path.parent.mkdir(parents=True, exist_ok=True)
        return None

    @event.listens_for(engine, "connect")
    def _enforce_foreign_keys(dbapi_connection, connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine
