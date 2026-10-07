import importlib.util
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy.engine import URL

from database.core.errors import (
    ConfigurationError,
    InactiveInstanceError,
    InvalidInputError,
)
from database.core.values import (
    DatabaseInstance,
    FilterCombination,
    OrderDirection,
)

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"

_INSTANCE_KEYS = (
    "name",
    "active",
    "engine",
    "host",
    "port",
    "database",
    "username",
    "password",
    "options",
)
_CONNECTION_VALUES = ("host", "port", "database", "username", "password")
_STORAGE_KINDS = ("file", "server")


@dataclass(frozen=True)
class Engine:
    key: str
    name: str
    driver: str
    parameters: Mapping[str, Any]


@dataclass(frozen=True)
class Instance:
    key: str
    name: str
    active: bool
    engine: str
    host: str | None
    port: int | None
    database: str
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True)
class QueryDefaults:
    combination: FilterCombination
    limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True)
class Preparation:
    enabled: bool
    fail_on_error: bool
    command: str


@dataclass(frozen=True)
class InitialDataGroup:
    entity: str
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class Configuration:
    engines: Mapping[str, Engine]
    instances: Mapping[str, Instance]
    default_instance: str
    storage_root: Path
    query: QueryDefaults
    preparation: Preparation
    initial_data: tuple[InitialDataGroup, ...]


@dataclass(frozen=True)
class Connection:
    """The complete connection of one Instance; it never leaves Core and Engine units."""

    instance: DatabaseInstance
    engine: str
    driver: str
    parameters: Mapping[str, Any]
    url: URL = field(repr=False)
    path: Path | None


def member_name(key: str) -> str:
    return key.upper()


def _fail(location: str, problem: str) -> ConfigurationError:
    return ConfigurationError(f"Invalid configuration: {location} {problem}.")


def _mapping(value: Any, location: str) -> Mapping[str, Any]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise _fail(location, "must be a mapping")
    return value


def _text(value: Any, location: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value:
        raise _fail(location, "must be a non-empty text")
    return value


def _boolean(value: Any, location: str) -> bool:
    if not isinstance(value, bool):
        raise _fail(location, "must be true or false")
    return value


def _integer(value: Any, location: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        raise _fail(location, "must be an integer")
    return value


def _member(enumeration: Any, value: Any, location: str) -> Any:
    if not isinstance(value, str) or value not in enumeration.__members__:
        raise _fail(location, "names an unknown enumeration member")
    return enumeration[value]


def _storage_root(value: Any) -> Path:
    text = _text(value, "settings.storage_root")
    root = (COMPONENT_ROOT / text).resolve()
    if not root.is_relative_to(COMPONENT_ROOT) or root == COMPONENT_ROOT:
        raise _fail("settings.storage_root", "must be a directory inside the Database")
    return root


def _engine(key: str, raw: Any) -> Engine:
    location = f"engines.{key}"
    body = _mapping(raw, location)
    parameters = _mapping(body.get("parameters"), f"{location}.parameters")
    _text(parameters.get("url_scheme"), f"{location}.parameters.url_scheme")
    storage = _mapping(parameters.get("storage"), f"{location}.parameters.storage")
    if storage.get("kind") not in _STORAGE_KINDS:
        raise _fail(f"{location}.parameters.storage.kind", "must be file or server")
    required = parameters.get("required_parameters")
    if not isinstance(required, list) or not all(item in _CONNECTION_VALUES for item in required):
        raise _fail(f"{location}.parameters.required_parameters", "must list connection values")
    return Engine(
        key=key,
        name=_text(body.get("name"), f"{location}.name"),
        driver=_text(body.get("driver"), f"{location}.driver"),
        parameters=parameters,
    )


def _instance(key: str, raw: Any, engines: Mapping[str, Engine]) -> Instance:
    location = f"instances.{key}"
    body = _mapping(raw, location)
    if set(body) != set(_INSTANCE_KEYS):
        raise _fail(location, "must hold exactly its complete definition")
    engine = _text(body["engine"], f"{location}.engine")
    if engine not in engines:
        raise _fail(f"{location}.engine", "names an unrecorded Engine")
    instance = Instance(
        key=key,
        name=_text(body["name"], f"{location}.name"),
        active=_boolean(body["active"], f"{location}.active"),
        engine=engine,
        host=_text(body["host"], f"{location}.host", nullable=True),
        port=_integer(body["port"], f"{location}.port", nullable=True),
        database=_text(body["database"], f"{location}.database"),
        username=_text(body["username"], f"{location}.username", nullable=True),
        password=body["password"],
        options=_mapping(body["options"], f"{location}.options"),
    )
    if instance.password is not None and not isinstance(instance.password, str):
        raise _fail(f"{location}.password", "must be text or null")
    if instance.active:
        for name in engines[engine].parameters["required_parameters"]:
            if getattr(instance, name) in (None, ""):
                raise _fail(f"{location}.{name}", "is required by its Engine")
    return instance


def _units_exist(engines: Mapping[str, Engine], instances: Mapping[str, Instance]) -> None:
    for instance in instances.values():
        if instance.active:
            spec = importlib.util.find_spec(f"database.engine.{instance.engine}")
            if spec is None:
                raise _fail(f"instances.{instance.key}.engine", "has no Engine unit")


def _initial_data(raw: Any) -> tuple[InitialDataGroup, ...]:
    if not isinstance(raw, list):
        raise _fail("initial_data", "must be a list")
    groups = []
    for index, item in enumerate(raw):
        location = f"initial_data[{index}]"
        body = _mapping(item, location)
        records = body.get("records")
        if not isinstance(records, list) or not all(isinstance(r, dict) for r in records):
            raise _fail(f"{location}.records", "must be a list of mappings")
        groups.append(
            InitialDataGroup(
                entity=_text(body.get("entity"), f"{location}.entity"),
                records=tuple(records),
            )
        )
    return tuple(groups)


def load_configuration(path: Path = CONFIGURATION_FILE) -> Configuration:
    """Load and validate a Database Configuration; no connection is opened."""
    try:
        with open(path, encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as error:
        raise ConfigurationError("The Database Configuration cannot be read.") from error
    body = _mapping(raw, "configuration")
    if set(body) != {"engines", "instances", "settings", "initial_data"}:
        raise _fail("configuration", "must hold exactly engines, instances, settings, initial_data")

    engines = {
        key: _engine(key, value) for key, value in _mapping(body["engines"], "engines").items()
    }
    instances = {
        key: _instance(key, value, engines)
        for key, value in _mapping(body["instances"], "instances").items()
    }
    names = [instance.name for instance in instances.values()]
    if len(set(names)) != len(names):
        raise _fail("instances", "must have unique names")
    members = [member_name(key) for key in instances]
    if len(set(members)) != len(members):
        raise _fail("instances", "must have unique public identities")
    active = {member_name(key) for key, instance in instances.items() if instance.active}
    if active != {member.name for member in DatabaseInstance}:
        raise _fail("instances", "must match the active DatabaseInstance members")
    _units_exist(engines, instances)

    settings = _mapping(body["settings"], "settings")
    default = _text(settings.get("default_instance"), "settings.default_instance")
    if default not in instances or not instances[default].active:
        raise _fail("settings.default_instance", "must name an active recorded Instance")
    query = _mapping(settings.get("query"), "settings.query")
    order = _mapping(query.get("default_order"), "settings.query.default_order")
    limit = _integer(query.get("default_limit"), "settings.query.default_limit")
    lifecycle = _mapping(settings.get("lifecycle"), "settings.lifecycle")
    after = _mapping(lifecycle.get("after_generation"), "settings.lifecycle.after_generation")
    command = after.get("command")
    if command != "prepare":
        raise _fail("settings.lifecycle.after_generation.command", "must name the preparation")
    return Configuration(
        engines=engines,
        instances=instances,
        default_instance=default,
        storage_root=_storage_root(settings.get("storage_root")),
        query=QueryDefaults(
            combination=_member(
                FilterCombination, query.get("filter_combination"), "settings.query"
            ),
            limit=limit if limit > 0 else -1,
            order_field=_text(order.get("field"), "settings.query.default_order.field"),
            order_direction=_member(
                OrderDirection, order.get("direction"), "settings.query.default_order"
            ),
        ),
        preparation=Preparation(
            enabled=_boolean(after.get("enabled"), "settings.lifecycle.after_generation.enabled"),
            fail_on_error=_boolean(
                after.get("fail_on_error"), "settings.lifecycle.after_generation.fail_on_error"
            ),
            command=command,
        ),
        initial_data=_initial_data(body["initial_data"]),
    )


CONFIGURATION = load_configuration()


def resolve_instance(
    selection: DatabaseInstance | None, configuration: Configuration = CONFIGURATION
) -> Instance:
    """Resolve the Instance of a call; fails before any storage is touched."""
    if selection is None:
        return configuration.instances[configuration.default_instance]
    if not isinstance(selection, DatabaseInstance):
        raise InvalidInputError("The Instance must be a DatabaseInstance member.")
    for key, instance in configuration.instances.items():
        if member_name(key) == selection.name:
            if not instance.active:
                raise InactiveInstanceError(f"The Instance {selection.name} is not active.")
            return instance
    raise ConfigurationError(f"The Instance {selection.name} is not configured.")


def resolve_connection(
    instance: Instance, configuration: Configuration = CONFIGURATION
) -> Connection:
    """Resolve the complete connection of an Instance from the configuration."""
    if not instance.active:
        raise InactiveInstanceError(f"The Instance {member_name(instance.key)} is not active.")
    member = DatabaseInstance.__members__.get(member_name(instance.key))
    if member is None:
        raise ConfigurationError(f"The Instance {member_name(instance.key)} is not configured.")
    engine = configuration.engines[instance.engine]
    parameters = engine.parameters
    scheme = parameters["url_scheme"]
    path = None
    if parameters["storage"]["kind"] == "file":
        path = (configuration.storage_root / instance.database).resolve()
        if parameters["storage"].get("reject_escape", True) and not path.is_relative_to(
            configuration.storage_root
        ):
            raise ConfigurationError(
                f"The storage of the Instance {member_name(instance.key)} is outside the Database."
            )
        url = URL.create(scheme, database=str(path))
    else:
        url = URL.create(
            scheme,
            username=instance.username,
            password=instance.password,
            host=instance.host,
            port=instance.port or parameters.get("default_port"),
            database=instance.database,
        )
    return Connection(
        instance=member,
        engine=instance.engine,
        driver=engine.driver,
        parameters=parameters,
        url=url,
        path=path,
    )
