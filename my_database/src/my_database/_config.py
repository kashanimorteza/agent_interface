"""Runtime configuration resolution: Engines, Instances, and the default Instance.

Reads only the non-secret layer-local configuration file. No connection object
or secret value is constructed or exposed here beyond what a Storage Adapter
needs internally.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_MODULE_DIR = Path(__file__).resolve().parent
_PACKAGE_ROOT = _MODULE_DIR.parent.parent
_CONFIG_PATH = _MODULE_DIR / "database.yaml"
_DATA_DIR = _PACKAGE_ROOT / "data"


@dataclass(frozen=True)
class EngineProfile:
    """A supported Database Engine profile."""

    key: str
    driver: str
    foreign_keys: bool
    check_same_thread: bool


@dataclass(frozen=True)
class InstanceDefinition:
    """One selectable Database Instance identity."""

    key: str
    name: str
    purpose: str
    engine_key: str
    database: str


class UnknownInstanceError(LookupError):
    """Raised when an explicit Instance selection does not match a configured Instance."""


class DatabaseConfig:
    """Resolved runtime configuration: Engines, Instances, and the default Instance."""

    def __init__(
        self,
        engines: dict[str, EngineProfile],
        instances: dict[str, InstanceDefinition],
        default_instance: str,
    ):
        if default_instance not in instances:
            raise ValueError(
                f"default_instance {default_instance!r} does not name a configured Instance"
            )
        self.engines = engines
        self.instances = instances
        self.default_instance = default_instance

    def resolve(self, instance_key: str | None) -> InstanceDefinition:
        """Resolve an explicit Instance selection, or the default when omitted."""
        key = instance_key or self.default_instance
        try:
            return self.instances[key]
        except KeyError:
            raise UnknownInstanceError(f"unknown Instance: {key!r}") from None

    def sqlalchemy_url(self, instance: InstanceDefinition) -> str:
        engine = self.engines[instance.engine_key]
        if engine.driver != "sqlite3":  # pragma: no cover - only SQLite is currently configured
            raise NotImplementedError(
                f"no URL builder registered for engine driver {engine.driver!r}"
            )
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        db_path = _DATA_DIR / f"{instance.database}.db"
        return f"sqlite:///{db_path}"


def load_config(path: Path | None = None) -> DatabaseConfig:
    raw = yaml.safe_load((path or _CONFIG_PATH).read_text())

    engines = {
        key: EngineProfile(
            key=key,
            driver=value["driver"],
            foreign_keys=value.get("foreign_keys", True),
            check_same_thread=value.get("check_same_thread", False),
        )
        for key, value in raw["engines"].items()
    }
    instances = {
        key: InstanceDefinition(
            key=key,
            name=value["name"],
            purpose=value["purpose"],
            engine_key=value["engine"],
            database=value["database"],
        )
        for key, value in raw["instances"].items()
    }
    return DatabaseConfig(
        engines=engines, instances=instances, default_instance=raw["default_instance"]
    )
