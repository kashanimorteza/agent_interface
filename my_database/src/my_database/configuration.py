"""Database Configuration: the declared Engines, Database Instances, and component Settings."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

_SECRET_SCHEMES = ("file:", "env:")
_EMPTY_INSTANCE = {"host": "", "port": "", "path": "", "username": "", "password": ""}


class ConfigurationError(Exception):
    """Raised when Database Configuration breaks its structure or its integrity rules."""


@dataclass(frozen=True, slots=True)
class EngineConfiguration:
    """One supported Engine and its Engine-specific parameters.

    Attributes:
        key (str): Engine key that Database Instances name.
        name (str): Human-readable Engine name.
        driver (str): Engine driver or dialect.
        parameters (dict[str, Any]): Engine-specific configuration.
    """

    key: str
    name: str
    driver: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class InstanceConfiguration:
    """One named Database Instance using one declared Engine.

    Attributes:
        key (str): Database Instance key that requests name.
        name (str): Human-readable Database Instance name.
        purpose (str): What the Database Instance stores.
        engine (str): Key of the declared Engine it uses.
        database (str): Database identity.
        host (str): Host, empty when the Engine needs none.
        port (str): Port, empty when the Engine needs none.
        path (str): Storage location relative to the configuration directory, empty when the Engine needs none.
        username (str): Connection username, empty when none.
        password (str): Connection password reference or value, empty when none.
        parameters (dict[str, Any]): Database Instance-specific configuration.
    """

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    host: str
    port: str
    path: str
    username: str
    password: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Settings:
    """Component-wide Database settings.

    Attributes:
        default_instance (str): Key of the Database Instance used when a request names none.
        assignments (dict[str, str]): Purpose key to Database Instance key.
        secrets (dict[str, str]): Secret key to a secret reference ('file:<location>' or 'env:<NAME>'), never a secret value.
        parameters (dict[str, Any]): Component-specific configuration.
    """

    default_instance: str
    assignments: dict[str, str]
    secrets: dict[str, str]
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Configuration:
    """The complete Database Configuration.

    Attributes:
        directory (Path): Directory of the configuration; relative locations resolve against it.
        engines (dict[str, EngineConfiguration]): Every supported Engine by key.
        instances (dict[str, InstanceConfiguration]): Every named Database Instance by key.
        settings (Settings): Component-wide settings.
    """

    directory: Path
    engines: dict[str, EngineConfiguration]
    instances: dict[str, InstanceConfiguration]
    settings: Settings

    @classmethod
    def load(cls, path: str | Path | None = None) -> Configuration:
        """Read and validate a Database Configuration.

        Args:
            path (str | Path, optional): Configuration location; the MY_DATABASE_CONFIG variable, then database.yaml in the working directory, are used when omitted.

        Returns:
            (Configuration): The validated configuration.
        """
        location = Path(
            path or os.environ.get("MY_DATABASE_CONFIG") or "database.yaml"
        ).resolve()
        raw = yaml.safe_load(location.read_text())
        if (
            not isinstance(raw, dict)
            or not isinstance(raw.get("engines"), dict)
            or not raw["engines"]
        ):
            raise ConfigurationError(
                "Database Configuration must declare at least one Engine under 'engines'."
            )
        engines = {
            key: EngineConfiguration(
                key, item["name"], item["driver"], dict(item.get("parameters") or {})
            )
            for key, item in raw["engines"].items()
        }
        if not isinstance(raw.get("instances"), dict) or not raw["instances"]:
            raise ConfigurationError(
                "Database Configuration must declare at least one Database Instance under 'instances'."
            )
        instances = {
            key: InstanceConfiguration(
                key,
                **{
                    **_EMPTY_INSTANCE,
                    **item,
                    "parameters": dict(item.get("parameters") or {}),
                },
            )
            for key, item in raw["instances"].items()
        }
        for instance in instances.values():
            if instance.engine not in engines:
                raise ConfigurationError(
                    f"Database Instance '{instance.key}' names undeclared Engine '{instance.engine}'."
                )
        raw_settings = raw.get("settings")
        if not isinstance(raw_settings, dict):
            raise ConfigurationError("Database Configuration must declare 'settings'.")
        settings = Settings(
            raw_settings["default_instance"],
            dict(raw_settings.get("assignments") or {}),
            dict(raw_settings.get("secrets") or {}),
            dict(raw_settings.get("parameters") or {}),
        )
        for name in (settings.default_instance, *settings.assignments.values()):
            if name not in instances:
                raise ConfigurationError(
                    f"Settings name undeclared Database Instance '{name}'."
                )
        for key, reference in settings.secrets.items():
            if not reference.startswith(_SECRET_SCHEMES):
                raise ConfigurationError(
                    f"Secret '{key}' must be a reference starting with 'file:' or 'env:', not a value."
                )
        return cls(location.parent, engines, instances, settings)

    def secret(self, key: str) -> str:
        """Resolve a secret reference to its value.

        Args:
            key (str): Secret key declared under the settings.

        Returns:
            (str): The secret value read from the referenced source.
        """
        scheme, _, target = self.settings.secrets[key].partition(":")
        if scheme == "env":
            return os.environ[target]
        return (self.directory / target).read_text().strip()
