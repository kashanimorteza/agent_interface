"""Resolves Database's runtime configuration from `database.yaml`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .paths import component_root


@dataclass(frozen=True, slots=True)
class EngineProfile:
    key: str
    driver: str
    url_scheme: str


@dataclass(frozen=True, slots=True)
class InstanceProfile:
    key: str
    name: str
    purpose: str
    engine: str
    database: str


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    engines: dict[str, EngineProfile]
    instances: dict[str, InstanceProfile]
    default_instance: str
    data_dir: Path | None = None
    """Overrides the default `database/data/` storage location; used by tests to isolate
    each run's file-backed Engine storage. `None` selects the default component-relative
    location."""

    def resolve_instance(self, name: str | None) -> InstanceProfile:
        from .exceptions import UnknownDatabaseInstance

        key = name or self.default_instance
        try:
            return self.instances[key]
        except KeyError:
            raise UnknownDatabaseInstance(
                f"No configured Database Instance named {key!r}"
            ) from None

    def storage_path(self, instance: InstanceProfile) -> Path:
        data_dir = self.data_dir or (component_root() / "data")
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / f"{instance.database}.db"


def load_runtime_config(path: Path | None = None) -> RuntimeConfig:
    config_path = path or (component_root() / "database.yaml")
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    engines = {
        key: EngineProfile(key=key, driver=value["driver"], url_scheme=value["url_scheme"])
        for key, value in raw["engines"].items()
    }
    instances = {
        key: InstanceProfile(
            key=key,
            name=value["name"],
            purpose=value["purpose"],
            engine=value["engine"],
            database=value["database"],
        )
        for key, value in raw["instances"].items()
    }
    default_instance = raw["default_instance"]
    if default_instance not in instances:
        raise ValueError(
            f"default_instance {default_instance!r} does not name a configured Instance"
        )
    return RuntimeConfig(engines=engines, instances=instances, default_instance=default_instance)
