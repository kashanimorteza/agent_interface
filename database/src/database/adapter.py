"""The Storage Adapter: owns connections to the selected Engine (Database Principle 1 & 2)."""

from __future__ import annotations

import sqlite3
import threading

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from database.config import RuntimeConfig, load_runtime_config, sqlite_url_for
from database.errors import UnknownInstanceError


@sa.event.listens_for(sa.engine.Engine, "connect")
def _enforce_sqlite_foreign_keys(dbapi_connection: object, _connection_record: object) -> None:
    """SQLite does not enforce foreign keys unless explicitly enabled per connection
    (Development Preferences `options.databases.SQLite.connection.foreign_keys`)."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class StorageAdapter:
    """Owns the Engine connection for every configured Instance, and the Session factory built
    on it. Consumers reach this only indirectly, through the Database Interface and Instance
    Registry (Database Principle 1) — this class is not itself part of the public surface."""

    def __init__(self, runtime_config: RuntimeConfig | None = None) -> None:
        self._runtime_config = runtime_config or load_runtime_config()
        self._engines: dict[str, sa.Engine] = {}
        self._session_factories: dict[str, sa_orm.sessionmaker[sa_orm.Session]] = {}
        self._lock = threading.Lock()

    @property
    def runtime_config(self) -> RuntimeConfig:
        return self._runtime_config

    def engine_for(self, instance_key: str | None) -> sa.Engine:
        instance = self._runtime_config.resolve(instance_key)
        with self._lock:
            engine = self._engines.get(instance.key)
            if engine is None:
                if instance.engine != "sqlite":
                    raise UnknownInstanceError(
                        f"Engine '{instance.engine}' has no Storage Adapter support."
                    )
                url = sqlite_url_for(instance)
                engine = sa.create_engine(url, connect_args={"check_same_thread": False})
                self._engines[instance.key] = engine
            return engine

    def session_factory_for(self, instance_key: str | None) -> sa_orm.sessionmaker[sa_orm.Session]:
        instance = self._runtime_config.resolve(instance_key)
        with self._lock:
            factory = self._session_factories.get(instance.key)
            if factory is None:
                factory = sa_orm.sessionmaker(bind=self.engine_for(instance.key))
                self._session_factories[instance.key] = factory
            return factory

    def new_session(self, instance_key: str | None = None) -> sa_orm.Session:
        return self.session_factory_for(instance_key)()
