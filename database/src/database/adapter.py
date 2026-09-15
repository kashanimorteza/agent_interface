"""The Storage Adapter.

Owns connections to the selected Engine and performs persistence
operations, resolving Database's own non-secret runtime configuration
(supported Engine profiles, configured Instances, and the default
Instance) from Database's layer-local runtime configuration file,
independent of process working directory.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy import event
from sqlalchemy.engine import Connection, Engine, create_engine
from sqlalchemy.exc import OperationalError

from database import observability
from database.mapping import MetaData, build_metadata

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = COMPONENT_ROOT / "database.yaml"
DEFAULT_DATA_DIR = COMPONENT_ROOT / "data"


class InstanceConfigurationError(ValueError):
    """A configured Instance or Engine reference is invalid or incomplete."""


class UnknownInstanceError(LookupError):
    """An explicit Instance selection does not name a configured Instance."""


@dataclass(frozen=True)
class InstanceConfig:
    """One configured, selectable database Instance."""

    key: str
    name: str
    purpose: str
    engine: str
    database: str


def _load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        msg = f"Database runtime configuration not found at {path}"
        raise InstanceConfigurationError(msg)
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def _sqlite_url(instance: InstanceConfig) -> str:
    DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = DEFAULT_DATA_DIR / f"{instance.database}.db"
    return f"sqlite:///{db_path}"


_URL_BUILDERS = {"sqlite": _sqlite_url}


class StorageAdapter:
    """Owns Engine connections for every configured Instance, keyed by stable Instance identity."""

    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        raw = _load_config(config_path)
        engines: dict[str, Any] = raw.get("engines") or {}
        instances_raw: dict[str, Any] = raw.get("instances") or {}
        if not instances_raw:
            msg = "No Instances configured in database.yaml"
            raise InstanceConfigurationError(msg)

        self._instances: dict[str, InstanceConfig] = {}
        for key, entry in instances_raw.items():
            engine_key = entry.get("engine")
            if engine_key not in engines:
                msg = f"Instance '{key}' references unknown engine '{engine_key}'"
                raise InstanceConfigurationError(msg)
            self._instances[key] = InstanceConfig(
                key=key,
                name=entry.get("name", key),
                purpose=entry.get("purpose", ""),
                engine=engine_key,
                database=entry.get("database", key),
            )

        default_key = raw.get("default_instance")
        if default_key not in self._instances:
            msg = (
                f"default_instance '{default_key}' does not name a configured Instance"
            )
            raise InstanceConfigurationError(msg)
        self._default_key: str = default_key

        self._metadata: MetaData = build_metadata()
        self._engines: dict[str, Engine] = {}

    @property
    def metadata(self) -> MetaData:
        return self._metadata

    @property
    def default_instance_key(self) -> str:
        return self._default_key

    def instances(self) -> tuple[InstanceConfig, ...]:
        return tuple(self._instances.values())

    def resolve_instance(self, instance_key: str | None) -> InstanceConfig:
        key = instance_key or self._default_key
        if key not in self._instances:
            raise UnknownInstanceError(key)
        return self._instances[key]

    def engine_for(self, instance_key: str | None = None) -> Engine:
        instance = self.resolve_instance(instance_key)
        if instance.key not in self._engines:
            builder = _URL_BUILDERS.get(instance.engine)
            if builder is None:
                msg = (
                    f"No portable URL builder registered for engine '{instance.engine}'"
                )
                raise InstanceConfigurationError(msg)
            url = builder(instance)
            connect_args: dict[str, Any] = {}
            if instance.engine == "sqlite":
                connect_args["check_same_thread"] = False
            engine = create_engine(url, future=True, connect_args=connect_args)
            if instance.engine == "sqlite":
                db_path = DEFAULT_DATA_DIR / f"{instance.database}.db"

                @event.listens_for(engine, "connect")
                def _set_sqlite_pragma(
                    dbapi_connection: Any, _connection_record: Any
                ) -> None:
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA foreign_keys = ON")
                    cursor.close()
                    # Least-privilege runtime access: SQLite has no server-side
                    # role system, so the file itself is restricted to the
                    # owning process user only.
                    if db_path.exists():
                        db_path.chmod(0o600)

            self._engines[instance.key] = engine
        return self._engines[instance.key]

    @contextmanager
    def connect(self, instance_key: str | None = None) -> Iterator[Connection]:
        """Yield a live connection scoped to one Instance; never falls back to another Instance on failure."""
        instance = self.resolve_instance(instance_key)
        engine = self.engine_for(instance.key)
        try:
            with engine.connect() as connection:
                yield connection
        except OperationalError as error:
            observability.record_connection_failure(instance.key, error)
            raise
