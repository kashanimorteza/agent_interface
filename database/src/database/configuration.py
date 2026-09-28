"""Load the Database Configuration: the Engines, named Instances, and Settings that Database can use."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from database.engine import IMPLEMENTED

CONFIGURATION_ENVIRONMENT_VARIABLE = "DATABASE_CONFIGURATION"
DEFAULT_PATH = Path(__file__).resolve().parents[2] / "database.yaml"


class ConfigurationError(ValueError):
    """Raised when the Database Configuration is inconsistent."""


@dataclass(frozen=True, slots=True)
class EngineSettings:
    """Declared Engine.

    Attributes:
        key (str): Key of the Engine in the configuration.
        name (str): Human-readable name.
        driver (str): Driver or dialect of the Engine.
        parameters (dict[str, Any]): Engine-specific parameters.
    """

    key: str
    name: str
    driver: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class InstanceSettings:
    """Named Instance using one Engine.

    Attributes:
        key (str): Key of the Instance in the configuration.
        name (str): Human-readable name.
        purpose (str): What the Instance stores.
        engine (str): Key of the Engine the Instance uses.
        database (str): Database identity, the storage file name for a file-backed Engine.
        host (str): Host, or empty.
        port (str): Port, or empty.
        path (str): Storage path, or empty.
        username (str): Username, or empty.
        password (str): Password, or empty.
        parameters (dict[str, Any]): Instance-specific parameters.
    """

    key: str
    name: str
    purpose: str
    engine: str
    database: str
    host: str = ""
    port: str = ""
    path: str = ""
    username: str = ""
    password: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Settings:
    """Component-wide Database settings.

    Attributes:
        default_instance (str): Key of the Instance used when a request names none.
        assignments (dict[str, str]): Purpose key to Instance key.
        secrets (dict[str, str]): Secret key to secret reference.
        parameters (dict[str, Any]): Shared parameters, including the Database Directory and query defaults.
    """

    default_instance: str
    assignments: dict[str, str] = field(default_factory=dict)
    secrets: dict[str, str] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Configuration:
    """Complete Database Configuration.

    Attributes:
        path (Path): File the configuration was read from.
        engines (dict[str, EngineSettings]): Declared Engines by key.
        instances (dict[str, InstanceSettings]): Named Instances by key.
        settings (Settings): Component-wide settings.
    """

    path: Path
    engines: dict[str, EngineSettings]
    instances: dict[str, InstanceSettings]
    settings: Settings

    @property
    def root(self) -> Path:
        """Directory that relative storage locations resolve against."""
        return self.path.parent

    @property
    def filter_combination(self) -> str:
        """Filter combination List uses when none is requested."""
        return self.settings.parameters["query"]["filter_combination"]

    @property
    def default_order(self) -> dict[str, str]:
        """Order List uses when none is requested, with a `field` and a `direction`."""
        return self.settings.parameters["query"]["default_order"]

    def storage_path(self, instance: InstanceSettings) -> Path:
        """Return the storage location of a file-backed Instance.

        Args:
            instance (InstanceSettings): Instance whose storage is wanted.

        Returns:
            (Path): Location of the Instance's storage file.
        """
        directory = (
            self.root
            / self.settings.parameters.get("database_directory", "")
            / instance.path
        )
        return directory / instance.database


def resolve_path(path: Path | str | None = None) -> Path:
    """Return the configuration file to read.

    Args:
        path (Path | str, optional): Explicit configuration file.

    Returns:
        (Path): The explicit file, else the file named by the environment, else the Component's own file.
    """
    return Path(
        path or os.environ.get(CONFIGURATION_ENVIRONMENT_VARIABLE) or DEFAULT_PATH
    ).resolve()


def load(path: Path | str | None = None) -> Configuration:
    """Read the Database Configuration.

    Args:
        path (Path | str, optional): Explicit configuration file.

    Returns:
        (Configuration): The declared Engines, Instances, and Settings.
    """
    file = resolve_path(path)
    raw = yaml.safe_load(file.read_text())
    configuration = Configuration(
        path=file,
        engines={k: EngineSettings(key=k, **v) for k, v in raw["engines"].items()},
        instances={
            k: InstanceSettings(key=k, **v) for k, v in raw["instances"].items()
        },
        settings=Settings(**raw["settings"]),
    )
    validate(configuration)
    return configuration


def validate(configuration: Configuration) -> None:
    """Refuse a configuration whose Engines, Instances, and Settings do not resolve.

    Args:
        configuration (Configuration): Configuration to check.
    """
    for instance in configuration.instances.values():
        if instance.engine not in configuration.engines:
            raise ConfigurationError(
                f"Instance '{instance.key}' uses undeclared Engine '{instance.engine}'"
            )
    settings = configuration.settings
    for purpose, key in {
        "default": settings.default_instance,
        **settings.assignments,
    }.items():
        if key not in configuration.instances:
            raise ConfigurationError(
                f"Setting '{purpose}' names undeclared Instance '{key}'"
            )
    default_engine = configuration.instances[settings.default_instance].engine
    if default_engine not in IMPLEMENTED:
        raise ConfigurationError(
            f"The default Instance uses Engine '{default_engine}', which is not marked for implementation"
        )
