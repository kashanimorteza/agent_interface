"""The Storage Adapter foundation: Engine connections and runtime-configuration resolution.

Every later storage mapping and the Database Interface build on the single `StorageAdapter`
this module produces rather than resolving their own connection or configuration.
"""

from __future__ import annotations

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from . import observability
from .exceptions import ConnectionFailure
from .runtime_config import InstanceProfile, RuntimeConfig, load_runtime_config


class StorageAdapter:
    """Resolves one Database Instance's Engine connection and session factory."""

    def __init__(
        self,
        config: RuntimeConfig | None = None,
        *,
        instance: str | None = None,
        verify_schema: bool = True,
    ) -> None:
        self.config = config or load_runtime_config()
        self.instance: InstanceProfile = self.config.resolve_instance(instance)
        engine_profile = self.config.engines[self.instance.engine]

        db_path = self.config.storage_path(self.instance)
        url = f"{engine_profile.url_scheme}:///{db_path}"

        try:
            self.engine: Engine = create_engine(url, future=True)
            with self.engine.connect():
                pass
        except SQLAlchemyError as exc:
            observability.connection_failure(self.instance.key, str(exc.__class__.__name__))
            raise ConnectionFailure(
                f"Could not connect to Database Instance {self.instance.key!r}"
            ) from exc

        # Least-privilege runtime identity for a file-backed Engine: restrict the database
        # file to owner-only access rather than relying on OS-account privilege alone.
        if db_path.exists():
            db_path.chmod(0o600)

        self._session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

        if verify_schema:
            from . import schema

            schema.verify_no_drift(self.engine)

    def session(self) -> Session:
        return self._session_factory()


@event.listens_for(Engine, "connect")
def _enforce_foreign_keys(dbapi_connection: object, _connection_record: object) -> None:
    """Enable SQLite foreign-key enforcement, which is off by default per connection."""
    if type(dbapi_connection).__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
