"""The Storage gateway: one Action for every capability Database Interface publishes."""

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
    """Logic's gateway to Database; it adds nothing of its own."""

    def __init__(self) -> None:
        self._database = Database()

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Store one complete new Entity instance and return the stored Entity."""
        return self._database.add(entity, instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace every mutable Field of the stored record; null when no record exists."""
        return self._database.update(entity, instance)

    def list(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the Entities that match; a zero or negative limit means no limit."""
        return self._database.list(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: Any, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Return the Entity with the given id, or null."""
        return self._database.get_by_id(entity, id, instance)

    def delete(self, entity: Any, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Remove the record and return the final deleted Entity, or null."""
        return self._database.delete(entity, id, instance)

    def enable(self, entity: Any, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set only the activity Field to true and return the final Entity, or null."""
        return self._database.enable(entity, id, instance)

    def disable(self, entity: Any, id: int, instance: DatabaseInstance | None = None) -> Any:
        """Set only the activity Field to false and return the final Entity, or null."""
        return self._database.disable(entity, id, instance)

    def count(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._database.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls, or zero."""
        return self._database.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or null."""
        return self._database.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls, or null."""
        return self._database.max(entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._database.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Run a native command in the Instance Engine's query language."""
        return self._database.execute_command(command, parameters, instance)

    def create_tables(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Create every Table from the Model Entities; stop on a difference with an existing one."""
        return self._database.create_tables(instance)

    def insert_initial_data(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Insert every missing configured Initial Data record; skip identical present ones."""
        return self._database.insert_initial_data(instance)

    def prepare(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Run create_tables and then insert_initial_data; stop if create_tables fails."""
        return self._database.prepare(instance)
