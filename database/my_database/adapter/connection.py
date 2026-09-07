"""Engine connections for the defined Instances.

The adapter owns the connection to the resolved Engine. It hands connections
to the Data Logic layer only; nothing here is published to consumers.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import Connection, Engine, create_engine, event
from sqlalchemy.engine import URL

from ..errors import ConfigurationError
from ..runtime import DatabaseSettings, InstanceSettings
from .instances import InstanceCollection

DEFAULT_PORTS = {"PostgreSQL": 5432, "MySQL": 3306}
DRIVERS = {"PostgreSQL": "postgresql+psycopg", "MySQL": "mysql+pymysql"}


class StorageAdapter:
    """Opens and caches one Engine per Instance."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self.instances = InstanceCollection(settings)
        self._engines: dict[str, Engine] = {}

    # -- URL resolution ----------------------------------------------------

    def storage_path(self, key: str | None = None):
        """The storage file of a file-based Instance; None for a server Engine."""
        raw = self.instances.settings_for(key)
        if raw.engine != "SQLite":
            return None
        return self._settings.storage_directory / f"{raw.database}.sqlite"

    def url(self, key: str | None = None) -> URL:
        raw = self.instances.settings_for(key)
        if raw.engine == "SQLite":
            path = self.storage_path(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            return URL.create("sqlite", database=str(path))
        port = raw.port if isinstance(raw.port, int) else DEFAULT_PORTS[raw.engine]
        return URL.create(
            DRIVERS[raw.engine],
            username=self._settings.secret(raw.username_secret),
            password=self._settings.secret(raw.password_secret),
            host=raw.host,
            port=port,
            database=raw.database,
            query={"charset": "utf8mb4"} if raw.engine == "MySQL" else {},
        )

    # -- engines -----------------------------------------------------------

    def engine(self, key: str | None = None) -> Engine:
        resolved = self.instances.resolve_key(key)
        engine = self._engines.get(resolved)
        if engine is None:
            raw = self.instances.settings_for(resolved)
            engine = self._create_engine(raw, self.url(resolved))
            self._engines[resolved] = engine
        return engine

    @staticmethod
    def _create_engine(raw: InstanceSettings, url: URL) -> Engine:
        if raw.engine == "SQLite":
            engine = create_engine(url, connect_args={"check_same_thread": False})

            @event.listens_for(engine, "connect")
            def _enforce_foreign_keys(dbapi_connection, _record) -> None:  # noqa: ANN001
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            return engine
        try:
            return create_engine(url)
        except Exception as exc:  # driver missing or URL invalid
            raise ConfigurationError(f"cannot create engine for {raw.key!r}: {exc}") from exc

    @contextmanager
    def connect(self, key: str | None = None) -> Iterator[Connection]:
        """A transactional connection to the selected (or default) Instance."""
        with self.engine(key).begin() as connection:
            yield connection

    def dispose(self) -> None:
        for engine in self._engines.values():
            engine.dispose()
        self._engines.clear()
