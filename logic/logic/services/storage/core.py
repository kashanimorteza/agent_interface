"""Storage core: the one gateway through which Logic reaches every public Database capability."""

import builtins
from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Any

from database.interface import (
    CommandResult,
    Database,
    Filter,
    FilterCombination,
    LifecycleResult,
    Order,
)
from sqlmodel import SQLModel


class Storage:
    """Logic's gateway to Database: one Action for every public Database capability, each passing its request through unchanged.

    Creating a gateway takes one Database access and opens no connection; every Action uses that same access.
    """

    def __init__(self) -> None:
        self._database = Database()

    def add[E: SQLModel](self, entity: E, instance: Enum | None = None) -> E:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        return self._database.add(entity, instance)

    def update[E: SQLModel](self, entity: E, instance: Enum | None = None) -> E | None:
        """Replace every mutable Field of the record the Entity's id locates; null when there is none."""
        return self._database.update(entity, instance)

    def list[E: SQLModel](
        self,
        entity: type[E],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: Enum | None = None,
    ) -> builtins.list[E]:
        """The matching Entities, ordered and limited; a limit of zero or below means no limit."""
        return self._database.list(
            entity, filters, combination, orders, limit, instance
        )

    def get_by_id[E: SQLModel](
        self, entity: type[E], id: int, instance: Enum | None = None
    ) -> E | None:
        """The Entity with the given id, or null when there is none."""
        return self._database.get_by_id(entity, id, instance)

    def delete[E: SQLModel](
        self, entity: type[E], id: int, instance: Enum | None = None
    ) -> E | None:
        """Remove the record with the given id and return it as it was; null when there is none."""
        return self._database.delete(entity, id, instance)

    def enable[E: SQLModel](
        self, entity: type[E], id: int, instance: Enum | None = None
    ) -> E | None:
        """Set only the activity flag to active; the final Entity, or null when there is none."""
        return self._database.enable(entity, id, instance)

    def disable[E: SQLModel](
        self, entity: type[E], id: int, instance: Enum | None = None
    ) -> E | None:
        """Set only the activity flag to inactive; the final Entity, or null when there is none."""
        return self._database.disable(entity, id, instance)

    def count(
        self,
        entity: type[SQLModel],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> int:
        """The number of matching records."""
        return self._database.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type[SQLModel],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The total of one numeric Field, ignoring nulls; zero when nothing matches."""
        return self._database.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: type[SQLModel],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The smallest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return self._database.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: type[SQLModel],
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The largest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return self._database.max(entity, field, filters, combination, instance)

    def truncate(self, entity: type[SQLModel], instance: Enum | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the number removed."""
        return self._database.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: Enum | None = None,
    ) -> CommandResult:
        """Run one native command in the Instance Engine's query language with bound parameters."""
        return self._database.execute_command(command, parameters, instance)

    def create_tables(self, instance: Enum | None = None) -> LifecycleResult:
        """Create every Table of the Model's Entities; matching Tables are left unchanged."""
        return self._database.create_tables(instance)

    def insert_initial_data(self, instance: Enum | None = None) -> LifecycleResult:
        """Insert every configured Initial Data record that is not already stored."""
        return self._database.insert_initial_data(instance)

    def prepare(self, instance: Enum | None = None) -> LifecycleResult:
        """Run create_tables and then insert_initial_data; stop when create_tables fails."""
        return self._database.prepare(instance)
