"""Resolution of Database's own non-secret runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PACKAGE_ROOT / "database.yaml"


@dataclass(frozen=True)
class InstanceConfig:
    key: str
    name: str
    purpose: str
    engine: str
    database: str


def _load_raw() -> dict:
    with open(_CONFIG_PATH) as f:
        return yaml.safe_load(f)


def load_instances() -> dict[str, InstanceConfig]:
    raw = _load_raw()
    instances = {}
    for key, entry in raw["instances"].items():
        instances[key] = InstanceConfig(
            key=key,
            name=entry["name"],
            purpose=entry["purpose"],
            engine=entry["engine"],
            database=entry["database"],
        )
    return instances


def default_instance_key() -> str:
    raw = _load_raw()
    default = raw["default_instance"]
    instances = raw["instances"]
    if default not in instances:
        raise ValueError(f"Configured default_instance {default!r} does not name a configured Instance.")
    return default


def sqlite_storage_path(instance: InstanceConfig) -> Path:
    """The physical file location for a SQLite-backed Instance, resolved from code_path."""
    return _PACKAGE_ROOT / "data" / f"{instance.database}.db"
