"""Load and validate the Database Configuration."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from database.core.vocabulary import (
    DatabaseInstance,
    FilterCombination,
    Order,
    OrderDirection,
)

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIGURATION = PACKAGE_ROOT / "config.yaml"


@dataclass(frozen=True, slots=True)
class EngineConfig:
    """One supported Engine.

    Attributes:
        key: Engine key.
        name: Human-readable Engine name.
        driver: Engine driver or dialect.
        parameters: Engine-specific parameters.
    """

    key: str
    name: str
    driver: str
    parameters: dict[str, Any]


@dataclass(frozen=True, slots=True)
class InstanceConfig:
    """One named Instance.

    Attributes:
        key: Instance key.
        name: Human-readable Instance name.
        active: Whether Interface publishes the Instance.
        purpose: What the Instance stores.
        engine: Key of the Engine the Instance uses.
        database: Database identity.
        host: Host or empty.
        port: Port or empty.
        path: Storage path relative to the Database package, or empty.
        username: Username or empty.
        password: Password or empty.
        parameters: Instance-specific parameters.
    """

    key: str
    name: str
    active: bool
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
class QueryDefaults:
    """Query defaults resolved to runtime values.

    Attributes:
        combination: Filter Combination used when a request omits one.
        order: Order used when List omits Orders.
        limit: Limit used when List omits one; zero or less means no limit.
    """

    combination: FilterCombination
    order: Order
    limit: int


@dataclass(frozen=True, slots=True)
class Configuration:
    """The declared Engines, Instances, and component Settings.

    Attributes:
        engines: Engines by key.
        instances: Instances by key.
        default_instance: Key of the default Instance.
        parameters: Component-specific Settings.
        query_defaults: Query defaults resolved to runtime values.
    """

    engines: dict[str, EngineConfig]
    instances: dict[str, InstanceConfig]
    default_instance: str
    parameters: dict[str, Any]
    query_defaults: QueryDefaults

    @property
    def active_instances(self) -> tuple[str, ...]:
        """Return the keys of the active Instances in declared order."""
        return tuple(key for key, instance in self.instances.items() if instance.active)

    @property
    def default(self) -> DatabaseInstance:
        """Return the default Instance as its Instance Enum member."""
        return DatabaseInstance(self.default_instance)


def load_configuration(path: Path = DEFAULT_CONFIGURATION) -> Configuration:
    """Load a Database Configuration and refuse one that breaks its integrity conditions.

    Args:
        path (Path): Configuration file to load.

    Returns:
        (Configuration): The validated Configuration.
    """
    raw = yaml.safe_load(path.read_text())
    engines = {
        key: EngineConfig(key=key, **value) for key, value in raw["engines"].items()
    }
    instances = {
        key: InstanceConfig(key=key, **value) for key, value in raw["instances"].items()
    }
    configuration = Configuration(
        engines=engines,
        instances=instances,
        default_instance=raw["settings"]["default_instance"],
        parameters=raw["settings"]["parameters"],
        query_defaults=_query_defaults(raw["settings"]["parameters"]),
    )
    _validate(configuration)
    return configuration


def _validate(configuration: Configuration) -> None:
    errors = [
        f"Instance {key} names undeclared Engine {instance.engine}"
        for key, instance in configuration.instances.items()
        if instance.engine not in configuration.engines
    ]
    default = configuration.instances.get(configuration.default_instance)
    if default is None:
        errors.append(
            f"default Instance {configuration.default_instance} is not declared"
        )
    elif not default.active:
        errors.append(f"default Instance {configuration.default_instance} is inactive")
    members = tuple(member.value for member in DatabaseInstance)
    if set(configuration.active_instances) != set(members):
        errors.append(
            f"Instance Enum members {sorted(members)} differ from active Instances "
            f"{sorted(configuration.active_instances)}"
        )
    if errors:
        raise ValueError("\n".join(errors))


def _query_defaults(parameters: dict[str, Any]) -> QueryDefaults:
    default_order = parameters["default_order"]
    return QueryDefaults(
        combination=FilterCombination(parameters["filter_combination"]),
        order=Order(default_order["field"], OrderDirection(default_order["direction"])),
        limit=int(parameters["default_limit"]),
    )
