"""Storage Actions: one Action for every capability Database Interface publishes, each passing its request and answer through unchanged."""

from collections.abc import Mapping, Sequence
from typing import Any

from database.interface import (
    CommandResult,
    Database,
    DatabaseInstance,
    Filter,
    FilterCombination,
    LifecycleResult,
    Order,
)


def storage_add(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Store one complete new Entity instance and return the stored Entity."""
    return Database().add(entity, instance)


def storage_update(entity: Any, instance: DatabaseInstance | None = None) -> Any:
    """Replace the mutable Fields of the stored record the Entity's id locates; return the stored Entity or None."""
    return Database().update(entity, instance)


def storage_list(
    entity: type[Any],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    orders: Sequence[Order] | None = None,
    limit: int | None = None,
    instance: DatabaseInstance | None = None,
) -> Sequence[Any]:
    """Return the Entities that match, ordered and limited; a zero or negative limit means no limit."""
    return Database().list(entity, filters, combination, orders, limit, instance)


def storage_get_by_id(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Return the Entity with the id, or None when none exists."""
    return Database().get_by_id(entity, id, instance)


def storage_delete(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Delete the record with the id and return it as it was, or None when none exists."""
    return Database().delete(entity, id, instance)


def storage_enable(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Set only is_active to true and return the final Entity, or None when none exists."""
    return Database().enable(entity, id, instance)


def storage_disable(
    entity: type[Any], id: Any, instance: DatabaseInstance | None = None
) -> Any:
    """Set only is_active to false and return the final Entity, or None when none exists."""
    return Database().disable(entity, id, instance)


def storage_count(
    entity: type[Any],
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> int:
    """Return how many Entities match."""
    return Database().count(entity, filters, combination, instance)


def storage_sum(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
    return Database().sum(entity, field, filters, combination, instance)


def storage_min(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
    return Database().min(entity, field, filters, combination, instance)


def storage_max(
    entity: type[Any],
    field: Any,
    filters: Sequence[Filter] | None = None,
    combination: FilterCombination | None = None,
    instance: DatabaseInstance | None = None,
) -> Any:
    """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
    return Database().max(entity, field, filters, combination, instance)


def storage_truncate(
    entity: type[Any], instance: DatabaseInstance | None = None
) -> int:
    """Remove every record of the Entity, keep its Table, and return the deleted count."""
    return Database().truncate(entity, instance)


def storage_execute_command(
    command: str,
    parameters: Mapping[str, Any] | Sequence[Any] | None = None,
    instance: DatabaseInstance | None = None,
) -> CommandResult:
    """Run a native command in the Instance Engine's query language with bound parameters."""
    return Database().execute_command(command, parameters, instance)


def storage_create_tables(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Create every Table from the Model Entities; Database stops on a difference with an existing Table."""
    return Database().create_tables(instance)


def storage_insert_initial_data(
    instance: DatabaseInstance | None = None,
) -> LifecycleResult:
    """Insert every missing Initial Data record, skipping identical records and failing on a conflict."""
    return Database().insert_initial_data(instance)


def storage_prepare(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Run Create Tables and then Insert Initial Data, stopping when Create Tables fails."""
    return Database().prepare(instance)
