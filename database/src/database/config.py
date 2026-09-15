"""Runtime storage configuration (Storage Adapter).

Loads and validates ``database.yaml`` — Database's own layer-local, non-secret
runtime settings — and resolves the file-backed storage location for the
selected Instance, independent of process working directory. No secret value
is ever read from this file; a reversible-encryption key comes only from the
runtime environment (see ``credentials.py``).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from database.exceptions import DatabaseConfigurationError

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PACKAGE_ROOT / "database.yaml"
DATA_DIR = PACKAGE_ROOT / "data"

SUPPORTED_ENGINES = {"sqlite"}


@dataclass(frozen=True, slots=True)
class InstanceConfig:
    key: str
    name: str
    purpose: str
    engine: str
    database: str


@dataclass(frozen=True, slots=True)
class StorageConfig:
    engines: tuple[str, ...]
    instances: dict[str, InstanceConfig]
    default_instance: str

    def resolve(self, instance: str | None) -> InstanceConfig:
        key = instance or self.default_instance
        try:
            return self.instances[key]
        except KeyError:
            from database.exceptions import UnknownInstanceError

            raise UnknownInstanceError(f"Unknown Instance {key!r}") from None

    def storage_path(self, instance: str | None = None) -> Path:
        cfg = self.resolve(instance)
        return DATA_DIR / f"{cfg.database}.db"


def load_storage_config(path: Path = CONFIG_PATH) -> StorageConfig:
    if not path.is_file():
        raise DatabaseConfigurationError(f"Runtime storage configuration not found at {path}")
    raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    engines = tuple((raw.get("engines") or {}).keys())
    for engine in engines:
        if engine not in SUPPORTED_ENGINES:
            raise DatabaseConfigurationError(f"Unsupported Engine {engine!r} declared in {path}")

    raw_instances = raw.get("instances") or {}
    if not raw_instances:
        raise DatabaseConfigurationError(f"No Instance declared in {path}")

    instances: dict[str, InstanceConfig] = {}
    for key, entry in raw_instances.items():
        engine = entry.get("engine")
        if engine not in engines:
            raise DatabaseConfigurationError(
                f"Instance {key!r} references undeclared Engine {engine!r}"
            )
        instances[key] = InstanceConfig(
            key=key,
            name=entry["name"],
            purpose=entry["purpose"],
            engine=engine,
            database=entry["database"],
        )

    default_instance = raw.get("default_instance")
    if default_instance not in instances:
        raise DatabaseConfigurationError(
            f"default_instance {default_instance!r} does not name a configured Instance"
        )

    return StorageConfig(engines=engines, instances=instances, default_instance=default_instance)


def sqlite_url(instance: str | None = None, config: StorageConfig | None = None) -> str:
    cfg = config or load_storage_config()
    path = cfg.storage_path(instance)
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{path}"
