"""SQLAlchemy engine and session factory for the configured SQLite file.

One engine is cached per database URL so processes that point at a different
file (for example a verification database) get their own engine. Foreign-key
enforcement is switched on for every new connection.
"""

from __future__ import annotations

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from ta_database.settings import get_settings

_engines: dict[str, Engine] = {}
_factories: dict[str, sessionmaker[Session]] = {}


def _enable_foreign_keys(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
    finally:
        cursor.close()


def get_engine(database_url: str | None = None) -> Engine:
    url = database_url or get_settings().database_url
    engine = _engines.get(url)
    if engine is None:
        connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
        engine = create_engine(url, connect_args=connect_args, future=True)
        if url.startswith("sqlite"):
            event.listen(engine, "connect", _enable_foreign_keys)
        _engines[url] = engine
    return engine


def get_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    url = database_url or get_settings().database_url
    factory = _factories.get(url)
    if factory is None:
        factory = sessionmaker(bind=get_engine(url), expire_on_commit=False, future=True)
        _factories[url] = factory
    return factory
