"""The settings this layer owns, and the check that they hold together.

The engine catalogue, the Instances and the default are read from the layer's
own settings file, found from where this layer lives rather than from wherever a
process happens to be running. Nothing here is served to a consumer: what a
consumer may see is derived from it, one layer up.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..contract import ConfigurationError

SETTINGS_NAME = "database.yaml"
SETTINGS_VARIABLE = "MY_DATABASE_SETTINGS"
DATA_VARIABLE = "MY_DATABASE_DATA"

_PACKAGE = Path(__file__).resolve().parents[1]
_SOURCE_ROOT = _PACKAGE.parent


def settings_file() -> Path:
    """Where this layer's own settings are, wherever the layer is running from.

    Running from the source tree they sit beside the package; installed, the
    copy built into it is used; and a deployment that keeps them somewhere else
    says so by name, which is how they are delivered to the layer without any
    other layer owning them.
    """

    delivered = os.environ.get(SETTINGS_VARIABLE)
    if delivered:
        return Path(delivered).expanduser().resolve()

    beside_the_package = _SOURCE_ROOT / SETTINGS_NAME
    if beside_the_package.exists():
        return beside_the_package
    return _PACKAGE / SETTINGS_NAME


def layer_root() -> Path:
    """The directory this layer keeps its own things in."""

    return settings_file().parent


def data_directory() -> Path:
    """Where a file-backed engine keeps its data, never the caller's directory."""

    chosen = os.environ.get(DATA_VARIABLE)
    return Path(chosen).expanduser().resolve() if chosen else layer_root() / "data"


@dataclass(frozen=True, slots=True)
class EngineProfile:
    """One engine this layer has an adapter for."""

    key: str
    driver: str
    storage: str
    url_scheme: str
    parameters: tuple[str, ...] = ()
    connection: dict[str, Any] = field(default_factory=dict)
    requires_secrets: tuple[str, ...] = ()

    @property
    def is_file_backed(self) -> bool:
        return self.storage == "file"


@dataclass(frozen=True, slots=True)
class InstanceSetting:
    """One stored identity, and how this layer reaches it."""

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    connection: dict[str, Any] = field(default_factory=dict)
    secrets: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Configuration:
    """Everything this layer owns, once it has been read and checked."""

    engines: dict[str, EngineProfile]
    instances: dict[str, InstanceSetting]
    default_instance: str
    declared_secrets: tuple[str, ...] = ()

    def instance(self, key: str | None) -> InstanceSetting:
        """The Instance to act on, refusing a named one nobody declared.

        An omitted selection uses the default. A named one that does not exist
        is refused rather than quietly answered with the default.
        """

        if key is None:
            return self.instances[self.default_instance]
        if key not in self.instances:
            known = ", ".join(sorted(self.instances)) or "none"
            raise ConfigurationError(
                f"no Instance named {key!r} is declared; declared Instances are {known}"
            )
        return self.instances[key]

    def profile_for(self, instance: InstanceSetting) -> EngineProfile:
        return self.engines[instance.engine]


def _read(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigurationError(f"this layer's settings file is missing at {path}")
    loaded = yaml.safe_load(path.read_text()) or {}
    if not isinstance(loaded, dict):
        raise ConfigurationError(f"this layer's settings file does not hold settings: {path}")
    return loaded


def load(path: Path | None = None) -> Configuration:
    """Read the layer's settings and refuse them if they do not hold together."""

    document = _read(path or settings_file())
    settings = document.get("settings") or {}

    engines = {
        key: EngineProfile(
            key=key,
            driver=values.get("driver", ""),
            storage=values.get("storage", ""),
            url_scheme=values.get("url_scheme", ""),
            parameters=tuple(values.get("parameters", ())),
            connection=dict(values.get("connection", {})),
            requires_secrets=tuple(values.get("requires_secrets", ())),
        )
        for key, values in (settings.get("engines") or {}).items()
    }

    instances = {
        key: InstanceSetting(
            key=key,
            name=values.get("name", ""),
            purpose=values.get("purpose", ""),
            engine=values.get("engine", ""),
            database=values.get("database", ""),
            connection=dict(values.get("connection", {})),
            secrets=dict(values.get("secrets", {})),
        )
        for key, values in (settings.get("instances") or {}).items()
    }

    configuration = Configuration(
        engines=engines,
        instances=instances,
        default_instance=settings.get("default_instance") or "",
        declared_secrets=tuple(document.get("secrets") or ()),
    )
    validate(configuration)
    return configuration


def validate(configuration: Configuration) -> None:
    """Refuse a configuration before anything is served on top of it."""

    if not configuration.instances:
        raise ConfigurationError("no Instance is declared")

    for instance in configuration.instances.values():
        if instance.engine not in configuration.engines:
            supported = ", ".join(sorted(configuration.engines)) or "none"
            raise ConfigurationError(
                f"Instance {instance.key!r} names engine {instance.engine!r}, "
                f"which this layer has no adapter for; supported engines are {supported}"
            )
        profile = configuration.engines[instance.engine]
        for parameter in profile.parameters:
            if not getattr(instance, parameter, None) and parameter not in instance.connection:
                raise ConfigurationError(
                    f"Instance {instance.key!r} is missing the setting {parameter!r}, "
                    f"which the {profile.key!r} engine requires"
                )
        for name in (*profile.requires_secrets, *instance.secrets.values()):
            if not name:
                raise ConfigurationError(
                    f"Instance {instance.key!r} refers to a secret with no name"
                )

    if not configuration.default_instance:
        raise ConfigurationError("no default Instance is selected")
    if configuration.default_instance not in configuration.instances:
        known = ", ".join(sorted(configuration.instances))
        raise ConfigurationError(
            f"the default Instance {configuration.default_instance!r} is not declared; "
            f"declared Instances are {known}"
        )
