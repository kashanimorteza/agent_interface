"""Data layer: resolves each request's Instance and Engine and routes the Operation.

Internal layer, not a consumer surface: use Database through ``database.interface``.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from functools import cache
from importlib import import_module
from pathlib import Path
from typing import Any

import yaml

_ROOT = Path(__file__).resolve().parents[2]
_CONFIGURATION = _ROOT / "database.yaml"
_engines: dict[tuple[Path, str], Any] = {}


@cache
def _load(path: Path) -> Mapping[str, Any]:
    with path.open() as stream:
        return yaml.safe_load(stream)


def configuration() -> Mapping[str, Any]:
    """The declared Engines, Instances, and Settings."""
    return _load(_CONFIGURATION)


@dataclass(frozen=True, slots=True)
class Resolved:
    """A request's Instance and the Engine implementation that serves it."""

    instance: str
    engine_key: str
    engine: Any


def resolve(instance: str | None = None) -> Resolved:
    """Resolve the named Instance, or the configured default Instance, and its Engine."""
    declared = configuration()
    key = instance if instance is not None else declared["settings"]["default_instance"]
    if key not in declared["instances"]:
        raise ValueError(f"Instance '{key}' is not declared")
    settings = declared["instances"][key]
    engine_key = settings["engine"]
    cache_key = (_CONFIGURATION, key)
    if cache_key not in _engines:
        module = import_module(f"database.engine.{engine_key}")
        directory = (
            _CONFIGURATION.parent
            / declared["settings"]["parameters"]["database_directory"]
        )
        parameters = declared["engines"][engine_key]["parameters"]
        _engines[cache_key] = module.Engine(settings, parameters, directory)
    return Resolved(key, engine_key, _engines[cache_key])


def _with_query_defaults(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Fill the configured default Filter Combination and Order when a List request omits them."""
    from database.interface import FilterCombination, Order, OrderDirection

    query = configuration()["settings"]["parameters"]["query"]
    filled = dict(kwargs)
    if filled.get("combination") is None:
        filled["combination"] = FilterCombination(query["filter_combination"])
    if not filled.get("orders"):
        default = query["default_order"]
        filled["orders"] = [
            Order(default["field"], OrderDirection(default["direction"]))
        ]
    return filled


def route(operation: str, instance: str | None, *args: Any, **kwargs: Any) -> Any:
    """Forward an Operation to the resolved Engine and return that Engine's result."""
    engine = resolve(instance).engine
    if operation == "list_":
        kwargs = _with_query_defaults(kwargs)
    return getattr(engine, operation)(*args, **kwargs)
