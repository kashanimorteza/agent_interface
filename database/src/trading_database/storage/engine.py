"""Engine and session factory — the only place the Storage Adapter opens the Database Engine."""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from trading_database.settings import get_settings

_engines: dict[str, Engine] = {}


def _is_sqlite(url: str) -> bool:
    return make_url(url).get_backend_name() == "sqlite"


def create_database_engine(url: str | None = None) -> Engine:
    """Create an Engine for ``url`` (default: the settings URL) with SQLite foreign keys enforced."""
    resolved = url or get_settings().database_url
    connect_args = {"check_same_thread": False} if _is_sqlite(resolved) else {}
    engine = create_engine(resolved, connect_args=connect_args)
    if _is_sqlite(resolved):

        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(dbapi_connection, _record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def get_engine() -> Engine:
    """The engine for the current settings URL, cached per URL."""
    url = get_settings().database_url
    engine = _engines.get(url)
    if engine is None:
        engine = _engines[url] = create_database_engine(url)
    return engine


def reset_engine() -> None:
    """Dispose every cached engine and clear the cache."""
    for engine in _engines.values():
        engine.dispose()
    _engines.clear()


def session_factory(engine: Engine | None = None) -> sessionmaker:
    """A sessionmaker bound to ``engine`` or to get_engine()."""
    return sessionmaker(bind=engine or get_engine(), expire_on_commit=False)
