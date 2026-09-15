"""The Storage Adapter: Engine connections and the Instance Registry.

Owns the only place Database opens a connection to a physical Engine. No
other module in this package creates an Engine directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import Engine, create_engine, event

_COMPONENT_ROOT = Path(__file__).resolve().parents[2]
_DATA_DIR = _COMPONENT_ROOT / "data"


@dataclass(frozen=True)
class InstanceIdentity:
    """One selectable database identity: a stable key, name, purpose, and Engine binding."""

    key: str
    name: str
    purpose: str
    engine: str
    database: str


class UnknownInstanceError(Exception):
    """Raised when an explicit Instance selection does not name a configured Instance."""


_INSTANCES: dict[str, InstanceIdentity] = {
    "general": InstanceIdentity(
        key="general",
        name="Trading Assistant General",
        purpose="General application data.",
        engine="sqlite",
        database="trading_assistant_general",
    ),
}
_DEFAULT_INSTANCE_KEY = "general"

_engines: dict[str, Engine] = {}


def instance_registry() -> list[dict[str, object]]:
    """Publish the selectable Instance identities and the default. No connections or secrets."""
    return [
        {
            "key": instance.key,
            "name": instance.name,
            "purpose": instance.purpose,
            "engine": instance.engine,
            "is_default": instance.key == _DEFAULT_INSTANCE_KEY,
        }
        for instance in _INSTANCES.values()
    ]


def default_instance_key() -> str:
    """The key of the Instance used when a caller omits an explicit selection."""
    return _DEFAULT_INSTANCE_KEY


def resolve_instance(instance_key: str | None) -> InstanceIdentity:
    """Resolve an explicit or omitted Instance selection to its configured identity."""
    key = instance_key or _DEFAULT_INSTANCE_KEY
    try:
        return _INSTANCES[key]
    except KeyError:
        raise UnknownInstanceError(key) from None


def _sqlite_url(instance: InstanceIdentity) -> str:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    db_path = _DATA_DIR / f"{instance.database}.db"
    return f"sqlite:///{db_path}"


def get_engine(instance_key: str | None = None) -> Engine:
    """Open (or reuse) the connection to the selected Instance's Engine."""
    instance = resolve_instance(instance_key)
    if instance.key not in _engines:
        engine = create_engine(
            _sqlite_url(instance), connect_args={"check_same_thread": False}
        )

        @event.listens_for(engine, "connect")
        def _enable_foreign_keys(
            dbapi_connection: object, _connection_record: object
        ) -> None:
            cursor = dbapi_connection.cursor()  # type: ignore[attr-defined]
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        _engines[instance.key] = engine
    return _engines[instance.key]


def component_root() -> Path:
    """The Database Component's repository-relative root, used to resolve file-backed storage."""
    return _COMPONENT_ROOT


def dispose_all_engines() -> None:
    """Close every cached Engine and forget it. Used to isolate tests that reset storage."""
    for engine in _engines.values():
        engine.dispose()
    _engines.clear()
