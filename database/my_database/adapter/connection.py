"""Engine connections for the declared Instances.

The adapter owns the connection to the selected Engine. It hands connections
to the Data Logic layer only; nothing here reaches a consumer. A failure to
reach one Instance is reported as such and never answered with another.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, Engine, create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

from ..config import DatabaseSettings, EngineProfile, InstanceProfile
from ..errors import ConnectionUnavailable
from .instances import InstanceCollection


class StorageAdapter:
    """Opens and caches one Engine per declared Instance."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self.instances = InstanceCollection(settings)
        self._engines: dict[str, Engine] = {}

    # -- storage location ----------------------------------------------------

    def storage_path(self, selection: Any = None) -> Path | None:
        """The storage file of a file-backed Instance, inside the code path."""
        profile = self.instances.profile(selection)
        if self._profile_of(profile).storage != "file":
            return None
        return self._settings.storage_directory / f"{profile.database}.db"

    def _profile_of(self, instance: InstanceProfile) -> EngineProfile:
        return self._settings.engines[instance.engine]

    # -- connection details --------------------------------------------------

    def url(self, selection: Any = None) -> URL:
        profile = self.instances.profile(selection)
        engine = self._profile_of(profile)
        if engine.storage == "file":
            path = self.storage_path(selection)
            path.parent.mkdir(parents=True, exist_ok=True)
            return URL.create(engine.url_scheme, database=str(path))
        port = profile.port if isinstance(profile.port, int) else engine.default_port
        query = {"charset": engine.charset} if engine.charset else {}
        return URL.create(
            engine.url_scheme,
            username=self._settings.secret(profile.username_secret),
            password=self._settings.secret(profile.password_secret),
            host=profile.host,
            port=port,
            database=profile.database,
            query=query,
        )

    # -- engines -------------------------------------------------------------

    def engine(self, selection: Any = None) -> Engine:
        key = self.instances.resolve_key(selection)
        engine = self._engines.get(key)
        if engine is None:
            profile = self.instances.profile(key)
            engine = self._create(self._profile_of(profile), self.url(key), key)
            self._engines[key] = engine
        return engine

    def _create(self, profile: EngineProfile, url: URL, key: str) -> Engine:
        try:
            if profile.storage == "file":
                engine = create_engine(url, connect_args={"check_same_thread": profile.check_same_thread})

                @event.listens_for(engine, "connect")
                def _prepare(dbapi_connection, _record) -> None:  # noqa: ANN001
                    cursor = dbapi_connection.cursor()
                    if profile.foreign_keys:
                        cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.execute(f"PRAGMA busy_timeout={int(profile.busy_timeout_ms)}")
                    cursor.close()

                return engine
            return create_engine(url)
        except Exception as exc:
            raise ConnectionUnavailable(f"Instance {key!r} cannot be reached: {exc}") from exc

    @contextmanager
    def connect(self, selection: Any = None) -> Iterator[Connection]:
        """A transactional connection to the selected, or default, Instance."""
        key = self.instances.resolve_key(selection)
        try:
            engine = self.engine(key)
            connection = engine.connect()
        except ConnectionUnavailable:
            raise
        except SQLAlchemyError as exc:
            raise ConnectionUnavailable(f"Instance {key!r} cannot be reached: {exc}") from exc
        with connection:
            with connection.begin():
                yield connection

    @contextmanager
    def open(self, selection: Any = None) -> Iterator[Connection]:
        """A connection whose transaction the caller controls."""
        key = self.instances.resolve_key(selection)
        try:
            connection = self.engine(key).connect()
        except ConnectionUnavailable:
            raise
        except SQLAlchemyError as exc:
            raise ConnectionUnavailable(f"Instance {key!r} cannot be reached: {exc}") from exc
        with connection:
            yield connection

    def dispose(self) -> None:
        for engine in self._engines.values():
            engine.dispose()
        self._engines.clear()
