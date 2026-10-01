"""Storage Core: the one gateway that holds one Database access and offers one Action per Database capability, in Database's order."""

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


class Storage:
    """Logic's gateway to Database: each Action hands its request to Database and returns the answer unchanged."""

    def __init__(self) -> None:
        self._database = Database()

    def add(
        self,
        entity: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Store one complete new Entity instance and return the stored Entity, including generated values."""
        return self._database.add(entity, instance)

    def update(
        self,
        entity: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Replace every mutable Field of the stored record the Entity's id locates; return the stored Entity or None."""
        return self._database.update(entity, instance)

    def delete(
        self,
        entity: type[Any],
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Delete the record with the id and return it as it was, or None when none exists."""
        return self._database.delete(entity, id, instance)

    def enable(
        self,
        entity: type[Any],
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Set only is_active to true and return the final Entity, or None when none exists."""
        return self._database.enable(entity, id, instance)

    def disable(
        self,
        entity: type[Any],
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Set only is_active to false and return the final Entity, or None when none exists."""
        return self._database.disable(entity, id, instance)

    def truncate(
        self,
        entity: type[Any],
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._database.truncate(entity, instance)

    def list(
        self,
        entity: type[Any],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return the Entities that match, ordered and limited; a zero or negative limit means no limit."""
        return self._database.list(
            entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self,
        entity: type[Any],
        id: Any,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the Entity with the id, or None when none exists."""
        return self._database.get_by_id(entity, id, instance)

    def count(
        self,
        entity: type[Any],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return how many Entities match."""
        return self._database.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type[Any],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls; zero when nothing matches."""
        return self._database.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: type[Any],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return self._database.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: type[Any],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls; None when nothing matches."""
        return self._database.max(entity, field, filters, combination, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Run a native command in the Instance Engine's query language with bound parameters."""
        return self._database.execute_command(command, parameters, instance)

    def create_tables(
        self,
        instance: DatabaseInstance | None = None,
    ) -> LifecycleResult:
        """Create every Table from the Model Entities; stop on a difference with an existing Table."""
        return self._database.create_tables(instance)

    def insert_initial_data(
        self,
        instance: DatabaseInstance | None = None,
    ) -> LifecycleResult:
        """Insert every missing Initial Data record, skipping identical records and failing on a conflict."""
        return self._database.insert_initial_data(instance)

    def prepare(
        self,
        instance: DatabaseInstance | None = None,
    ) -> LifecycleResult:
        """Run create_tables and then insert_initial_data, stopping when create_tables fails."""
        return self._database.prepare(instance)
