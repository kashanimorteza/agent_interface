"""Loading and validating the Database Configuration, the sole runtime source."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from model.interface import entities

from database.core.errors import ConfigurationError
from database.core.values import FilterCombination, OrderDirection, database_instance

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
CONFIGURATION_FILE = COMPONENT_ROOT / "config.yaml"

_SECTIONS = ("engines", "instances", "settings", "initial_data")
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


@dataclass(frozen=True, slots=True)
class ResolvedInstance:
    """One complete Instance with its Engine profile and resolved storage location."""

    key: str
    name: str
    active: bool
    engine: str
    driver: str
    parameters: Mapping[str, Any] = field(repr=False)
    host: str | None = field(repr=False)
    port: int | None = field(repr=False)
    database: str = field(repr=False)
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: Mapping[str, Any] = field(repr=False)
    location: Path | None = field(repr=False)


@dataclass(frozen=True, slots=True)
class QueryDefaults:
    """The resolved defaults of an omitted combination, Order set, or limit."""

    combination: FilterCombination
    limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True, slots=True)
class AfterGeneration:
    """The Setup behavior that follows generation."""

    enabled: bool
    fail_on_error: bool
    command: str


@dataclass(frozen=True, slots=True)
class InitialData:
    """The configured Initial Data records of one Entity."""

    entity: type
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    """The validated Database Configuration."""

    instances: Mapping[str, ResolvedInstance]
    default_instance: str
    storage_root: Path
    query: QueryDefaults
    after_generation: AfterGeneration
    initial_data: tuple[InitialData, ...]


def _mapping(value: Any) -> bool:
    return isinstance(value, Mapping) and all(isinstance(key, str) for key in value)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _member[E: (FilterCombination, OrderDirection)](
    kind: type[E], name: Any, where: str, problems: list[str]
) -> E | None:
    if isinstance(name, str) and name in kind.__members__:
        return kind[name]
    problems.append(f"{where} is not a {kind.__name__} member name")
    return None


def _engines(raw: Any, problems: list[str]) -> dict[str, Mapping[str, Any]]:
    if not _mapping(raw) or not raw:
        problems.append("engines must be a non-empty mapping")
        return {}
    engines: dict[str, Mapping[str, Any]] = {}
    for key, engine in raw.items():
        if not _mapping(engine) or set(engine) != {"name", "driver", "parameters"}:
            problems.append(
                f"engine {key!r} must hold exactly name, driver, parameters"
            )
        elif not _text(engine["name"]) or not _text(engine["driver"]):
            problems.append(f"engine {key!r} needs a name and a driver")
        elif not _mapping(engine["parameters"]):
            problems.append(f"engine {key!r} parameters must be a mapping")
        else:
            engines[key] = engine
    return engines


def _instances(
    raw: Any,
    engines: Mapping[str, Mapping[str, Any]],
    storage_root: Path | None,
    problems: list[str],
) -> dict[str, ResolvedInstance]:
    if not _mapping(raw) or not raw:
        problems.append("instances must be a non-empty mapping")
        return {}
    instances: dict[str, ResolvedInstance] = {}
    names: set[str] = set()
    for key, instance in raw.items():
        where = f"instance {key!r}"
        if not _mapping(instance) or set(instance) != set(_INSTANCE_KEYS):
            problems.append(f"{where} must hold exactly {', '.join(_INSTANCE_KEYS)}")
            continue
        found = len(problems)
        if not _text(instance["name"]) or instance["name"] in names:
            problems.append(f"{where} needs a unique name")
        if not isinstance(instance["active"], bool):
            problems.append(f"{where} active must be a boolean")
        engine = engines.get(instance["engine"])
        if engine is None:
            problems.append(f"{where} names no declared engine")
        for member in ("host", "username", "password"):
            if instance[member] is not None and not isinstance(instance[member], str):
                problems.append(f"{where} {member} must be text or null")
        if instance["port"] is not None and not _integer(instance["port"]):
            problems.append(f"{where} port must be an integer or null")
        if not isinstance(instance["database"], str):
            problems.append(f"{where} database must be text")
        if not _mapping(instance["options"]):
            problems.append(f"{where} options must be a mapping")
        if len(problems) > found or engine is None:
            continue
        names.add(instance["name"])
        parameters = engine["parameters"]
        if instance["active"]:
            for required in parameters.get("required_parameters", ()):
                if instance.get(required) in (None, ""):
                    problems.append(f"{where} needs a value for {required}")
        location = None
        if parameters.get("storage") == "file" and storage_root is not None:
            location = (storage_root / instance["database"]).resolve()
            if not instance["database"] or not location.is_relative_to(storage_root):
                problems.append(f"{where} storage location escapes the storage root")
                continue
            if location == storage_root:
                problems.append(f"{where} storage location is the storage root")
                continue
        instances[key] = ResolvedInstance(
            key=key,
            name=instance["name"],
            active=instance["active"],
            engine=instance["engine"],
            driver=engine["driver"],
            parameters=parameters,
            host=instance["host"],
            port=instance["port"],
            database=instance["database"],
            username=instance["username"],
            password=instance["password"],
            options=instance["options"],
            location=location,
        )
    return instances


def _storage_root(raw: Any, problems: list[str]) -> Path | None:
    if not _text(raw) or Path(raw).is_absolute():
        problems.append("settings.storage_root must be a relative directory")
        return None
    root = (COMPONENT_ROOT / raw).resolve()
    if not root.is_relative_to(COMPONENT_ROOT) or root == COMPONENT_ROOT:
        problems.append("settings.storage_root escapes the Database Component")
        return None
    return root


def _query(raw: Any, problems: list[str]) -> QueryDefaults | None:
    if not _mapping(raw) or set(raw) != {
        "filter_combination",
        "default_limit",
        "default_order",
    }:
        problems.append(
            "settings.query must hold filter_combination, default_limit, default_order"
        )
        return None
    combination = _member(
        FilterCombination,
        raw["filter_combination"],
        "settings.query.filter_combination",
        problems,
    )
    limit = raw["default_limit"]
    if not _integer(limit):
        problems.append("settings.query.default_limit must be an integer")
    order = raw["default_order"]
    if not _mapping(order) or set(order) != {"field", "direction"}:
        problems.append("settings.query.default_order must hold field and direction")
        return None
    direction = _member(
        OrderDirection,
        order["direction"],
        "settings.query.default_order.direction",
        problems,
    )
    for entity in entities:
        if order["field"] not in entity.model_fields:
            problems.append(
                f"settings.query.default_order.field is no Field of {entity.__name__}"
            )
    if combination is None or direction is None or not _integer(limit):
        return None
    return QueryDefaults(
        combination=combination,
        limit=limit if limit > 0 else -1,
        order_field=order["field"],
        order_direction=direction,
    )


def _after_generation(raw: Any, problems: list[str]) -> AfterGeneration | None:
    setup: Any = raw.get("after_generation") if _mapping(raw) else {}
    if (
        not _mapping(raw)
        or set(raw) != {"after_generation"}
        or not _mapping(setup)
        or set(setup) != {"enabled", "fail_on_error", "command"}
        or not isinstance(setup["enabled"], bool)
        or not isinstance(setup["fail_on_error"], bool)
        or setup["command"] != "prepare"
    ):
        problems.append(
            "settings.setup.after_generation must hold boolean enabled and "
            "fail_on_error and the command prepare"
        )
        return None
    return AfterGeneration(
        enabled=setup["enabled"],
        fail_on_error=setup["fail_on_error"],
        command=setup["command"],
    )


def _initial_data(raw: Any, problems: list[str]) -> tuple[InitialData, ...]:
    if not isinstance(raw, list):
        problems.append("initial_data must be a list")
        return ()
    by_name = {entity.__name__: entity for entity in entities}
    items: list[InitialData] = []
    seen: set[str] = set()
    for position, item in enumerate(raw):
        where = f"initial_data item {position}"
        if not _mapping(item) or set(item) != {"entity", "records"}:
            problems.append(f"{where} must hold exactly entity and records")
            continue
        entity = by_name.get(item["entity"])
        if entity is None or item["entity"] in seen:
            problems.append(f"{where} must name a Model Entity once")
            continue
        seen.add(item["entity"])
        records = item["records"]
        if not isinstance(records, list) or not all(map(_mapping, records)):
            problems.append(f"{where} records must be a list of Field mappings")
            continue
        items.append(InitialData(entity=entity, records=tuple(records)))
    return tuple(items)


def load(path: Path = CONFIGURATION_FILE) -> Configuration:
    """Read and validate the Database Configuration, failing before any connection."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError:
        raise ConfigurationError(
            "the Database Configuration is missing beside the Database package"
        ) from None
    except yaml.YAMLError:
        raise ConfigurationError(
            "the Database Configuration is not valid YAML"
        ) from None
    if not _mapping(raw) or set(raw) != set(_SECTIONS):
        raise ConfigurationError(
            "the Database Configuration must hold exactly " + ", ".join(_SECTIONS)
        )
    problems: list[str] = []
    settings = raw["settings"]
    if not _mapping(settings) or set(settings) != {
        "default_instance",
        "storage_root",
        "query",
        "setup",
    }:
        raise ConfigurationError(
            "settings must hold exactly default_instance, storage_root, query, setup"
        )
    storage_root = _storage_root(settings["storage_root"], problems)
    engines = _engines(raw["engines"], problems)
    instances = _instances(raw["instances"], engines, storage_root, problems)
    default = settings["default_instance"]
    if not isinstance(default, str) or default not in instances:
        problems.append("settings.default_instance names no valid Instance")
    elif not instances[default].active:
        problems.append("settings.default_instance names an inactive Instance")
    active = {key for key, instance in instances.items() if instance.active}
    if active != {member.value for member in database_instance}:
        problems.append(
            "the DatabaseInstance members differ from the active Instances; "
            "regenerate the Database Component"
        )
    query = _query(settings["query"], problems)
    after_generation = _after_generation(settings["setup"], problems)
    initial_data = _initial_data(raw["initial_data"], problems)
    if problems or storage_root is None or query is None or after_generation is None:
        raise ConfigurationError(
            "invalid Database Configuration: " + "; ".join(problems)
        )
    return Configuration(
        instances=instances,
        default_instance=default,
        storage_root=storage_root,
        query=query,
        after_generation=after_generation,
        initial_data=initial_data,
    )


@cache
def configuration() -> Configuration:
    """The validated Database Configuration, loaded once."""
    return load()
