"""Loads Database's own non-secret runtime configuration (Database Preferences
`settings.storage_adapter.runtime_configuration`)."""

from __future__ import annotations

import dataclasses
import pathlib

import yaml

from database.errors import UnknownInstanceError

_COMPONENT_ROOT = pathlib.Path(__file__).resolve().parents[2]
"""database/ — Development Preferences `selected.components.database.path`."""

DEFAULT_CONFIG_PATH = _COMPONENT_ROOT / "database.yaml"
DATA_DIRECTORY = _COMPONENT_ROOT / "data"
"""File-backed Engine storage location, relative to the Database Component root and independent
of process working directory (Database Preferences `settings.storage_adapter.storage_paths`)."""


@dataclasses.dataclass(frozen=True)
class InstanceConfig:
    key: str
    name: str
    purpose: str
    engine: str
    database: str


@dataclasses.dataclass(frozen=True)
class RuntimeConfig:
    instances: dict[str, InstanceConfig]
    default_instance: str

    def resolve(self, instance_key: str | None) -> InstanceConfig:
        """Resolve an explicit or omitted Instance selection (Database Principle 9): an omitted
        selection uses the default; an unknown explicit selection is rejected."""
        key = instance_key or self.default_instance
        if key not in self.instances:
            raise UnknownInstanceError(
                f"'{key}' does not name a configured Instance. "
                f"Configured Instances: {sorted(self.instances)}."
            )
        return self.instances[key]


def load_runtime_config(path: pathlib.Path = DEFAULT_CONFIG_PATH) -> RuntimeConfig:
    raw = yaml.safe_load(path.read_text())
    instances = {
        key: InstanceConfig(
            key=key,
            name=entry["name"],
            purpose=entry["purpose"],
            engine=entry["engine"],
            database=entry["database"],
        )
        for key, entry in raw["instances"].items()
    }
    default_instance = raw["default_instance"]
    if default_instance not in instances:
        raise UnknownInstanceError(
            f"default_instance '{default_instance}' does not name a configured Instance."
        )
    return RuntimeConfig(instances=instances, default_instance=default_instance)


def sqlite_url_for(instance: InstanceConfig) -> str:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    db_path = DATA_DIRECTORY / f"{instance.database}.db"
    return f"sqlite:///{db_path}"
