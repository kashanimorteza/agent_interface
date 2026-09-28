"""Route each request to the Engine of its resolved Instance.

Data resolves the Instance and its Engine, forwards the Operation, and returns the Engine's result.
"""

from collections.abc import Sequence
from pathlib import Path
from typing import Any

from database import configuration, engine, rules
from database.contract import Combination, CommandResult, Direction, Filter, Order

_configurations: dict[tuple[Path, int], configuration.Configuration] = {}
_engines: dict[tuple[Path, int, str], Any] = {}


def current_configuration() -> configuration.Configuration:
    """Return the Database Configuration, re-reading it when its file has changed."""
    path = configuration.resolve_path()
    key = (path, path.stat().st_mtime_ns)
    if key not in _configurations:
        _configurations[key] = configuration.load(path)
    return _configurations[key]


def resolve(instance: str | None = None) -> Any:
    """Return the Engine of a requested Instance.

    Args:
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (Any): The Engine implementation serving that Instance.
    """
    current = current_configuration()
    key = instance or current.settings.default_instance
    if key not in current.instances:
        raise ValueError(f"Unknown Instance '{key}'")
    cache_key = (current.path, current.path.stat().st_mtime_ns, key)
    if cache_key not in _engines:
        settings = current.instances[key]
        _engines[cache_key] = engine.load(settings.engine)(current, settings)
    return _engines[cache_key]


def forward(
    operation: str, instance: str | None, *arguments: Any, **keywords: Any
) -> Any:
    """Forward an Operation to the Engine of its Instance and return the Engine's result.

    Args:
        operation (str): Name of the Engine method that carries out the Operation.
        instance (str | None): Key of the requested Instance, or None for the default Instance.
        *arguments (Any): Positional arguments for the Engine method.
        **keywords (Any): Keyword arguments for the Engine method.

    Returns:
        (Any): The Engine's result.
    """
    return getattr(resolve(instance), operation)(*arguments, **keywords)


def add(entity: Any, instance: str | None = None) -> Any:
    """Store a new record and return the created Entity instance.

    Args:
        entity (Any): Entity instance for the new record.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (Any): The created Entity instance.
    """
    return forward("add", instance, rules.new_record(entity))


def update(entity: Any, instance: str | None = None) -> Any:
    """Change the supplied Fields of the record that has the instance's `id`.

    Args:
        entity (Any): Entity instance holding the `id` and the changed values.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (Any): The updated Entity instance, or None when no record has that `id`.
    """
    record_id, values = rules.update_values(entity)
    return forward("update", instance, type(entity), record_id, values)


def delete(entity_class: Any, record_id: Any, instance: str | None = None) -> bool:
    """Remove one record and report whether one was removed."""
    return forward("delete", instance, entity_class, record_id)


def enable(entity_class: Any, record_id: Any, instance: str | None = None) -> Any:
    """Activate one record and return it, or None when no record has that `id`."""
    return forward("enable", instance, entity_class, record_id)


def disable(entity_class: Any, record_id: Any, instance: str | None = None) -> Any:
    """Deactivate one record and return it, or None when no record has that `id`."""
    return forward("disable", instance, entity_class, record_id)


def list_(
    entity_class: Any,
    *,
    filters: Sequence[Filter] | None = None,
    filter_combination: Combination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: str | None = None,
) -> list[Any]:
    """Return the records of an Entity that satisfy the Filters, ordered and limited as requested.

    Args:
        entity_class (Any): Entity class to list.
        filters (Sequence[Filter], optional): Conditions on a record.
        filter_combination (Combination, optional): Combination enum member; the configured default when omitted.
        orders (Sequence[Order], optional): Ordering instructions; the configured default Order when omitted.
        limit (int, optional): Largest number of records to return; every match when omitted.
        instance (str, optional): Key of the Instance, or the default Instance when omitted.

    Returns:
        (list[Any]): Matching Entity instances.
    """
    if limit is not None and limit < 0:
        raise ValueError("limit cannot be negative")
    configured = current_configuration()
    order = configured.default_order
    return forward(
        "list_",
        instance,
        entity_class,
        list(filters or []),
        filter_combination or Combination(configured.filter_combination),
        list(
            orders
            or [Order(getattr(entity_class, order["field"]), Direction(order["direction"]))]
        ),
        limit,
    )


def truncate(entity_class: Any, instance: str | None = None) -> int:
    """Remove every record of an Entity and return how many were removed."""
    return forward("truncate", instance, entity_class)


def get_by_id(entity_class: Any, record_id: Any, instance: str | None = None) -> Any:
    """Return one record, or None when no record has that `id`."""
    return forward("get_by_id", instance, entity_class, record_id)


def count(entity_class: Any, instance: str | None = None) -> int:
    """Return the number of records of an Entity."""
    return forward("count", instance, entity_class)


def sum_(entity_class: Any, field: Any, instance: str | None = None) -> Any:
    """Return the total of a numeric Field, or 0 when no usable value exists."""
    return forward("sum_", instance, entity_class, field)


def min_(entity_class: Any, field: Any, instance: str | None = None) -> Any:
    """Return the smallest value of a Field, or None when no usable value exists."""
    return forward("min_", instance, entity_class, field)


def max_(entity_class: Any, field: Any, instance: str | None = None) -> Any:
    """Return the largest value of a Field, or None when no usable value exists."""
    return forward("max_", instance, entity_class, field)


def execute_command(
    command: str, parameters: Any = None, instance: str | None = None
) -> CommandResult:
    """Execute a SQL command through the Engine of the Instance and return its Command Result."""
    return forward("execute_command", instance, command, parameters)
