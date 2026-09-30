"""The only public Database boundary: one data-access gateway and its vocabulary."""

import builtins
from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from sqlmodel import SQLModel

from database.core import data
from database.core._contracts import (
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    LifecycleResult,
    Order,
    OrderDirection,
)
from database.core.initial_data import insert_initial_data
from database.core.tables import create_tables


class Database:
    """Entity Operations, the Database-wide Operation, and the Lifecycle Commands.

    Every capability accepts an optional DatabaseInstance and defaults to the
    configured default Instance.
    """

    # ------------------------------------------------------------- Entity Operations
    @staticmethod
    def add[E: SQLModel](entity: E, instance: DatabaseInstance | None = None) -> E:
        """Store a complete new Entity; return it with its generated values."""
        return data.add(entity, instance)

    @staticmethod
    def update[E: SQLModel](
        entity: E, instance: DatabaseInstance | None = None
    ) -> E | None:
        """Replace every mutable Field of the record with this id; None when missing."""
        return data.update(entity, instance)

    @staticmethod
    def list[E: SQLModel](
        entity: type[E],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> builtins.list[E]:
        """Return matching Entities, ordered (default id ascending) and limited."""
        return data.list_(entity, filters, combination, orders, limit, instance)

    @staticmethod
    def delete[E: SQLModel](
        entity: type[E], id: int, instance: DatabaseInstance | None = None
    ) -> E | None:
        """Delete the record and return the last deleted Entity; None when missing."""
        return data.delete(entity, id, instance)

    @staticmethod
    def enable[E: SQLModel](
        entity: type[E], id: int, instance: DatabaseInstance | None = None
    ) -> E | None:
        """Set only is_active to true; return the final Entity, or None."""
        return data.enable(entity, id, instance)

    @staticmethod
    def disable[E: SQLModel](
        entity: type[E], id: int, instance: DatabaseInstance | None = None
    ) -> E | None:
        """Set only is_active to false; return the final Entity, or None."""
        return data.disable(entity, id, instance)

    @staticmethod
    def get_by_id[E: SQLModel](
        entity: type[E], id: int, instance: DatabaseInstance | None = None
    ) -> E | None:
        """Return the Entity with this id, or None."""
        return data.get_by_id(entity, id, instance)

    @staticmethod
    def count(
        entity: type[SQLModel],
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return how many records match."""
        return data.count(entity, filters, combination, instance)

    @staticmethod
    def sum(
        entity: type[SQLModel],
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int | float | Decimal:
        """Return the total of a numeric Field, ignoring null; zero if none."""
        return data.sum_(entity, field, filters, combination, instance)

    @staticmethod
    def min(
        entity: type[SQLModel],
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the minimum of a Field, ignoring null; None if none."""
        return data.min_(entity, field, filters, combination, instance)

    @staticmethod
    def max(
        entity: type[SQLModel],
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the maximum of a Field, ignoring null; None if none."""
        return data.max_(entity, field, filters, combination, instance)

    @staticmethod
    def truncate(
        entity: type[SQLModel], instance: DatabaseInstance | None = None
    ) -> int:
        """Remove every record, keep the table, and return the deleted count."""
        return data.truncate(entity, instance)

    # -------------------------------------------------------- Database-wide Operation
    @staticmethod
    def execute_command(
        command: str,
        parameters: Mapping[str, Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Run any valid SQL command the selected Instance supports."""
        return data.execute_command(command, parameters, instance)

    # ------------------------------------------------------------ Lifecycle Commands
    @staticmethod
    def create_tables(instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Create or safely align every table the current Declarations require."""
        return create_tables(instance)

    @staticmethod
    def insert_initial_data(
        instance: DatabaseInstance | None = None,
    ) -> LifecycleResult:
        """Insert the shared Initial Data that is missing; safe to repeat."""
        return insert_initial_data(instance)


__all__ = [
    "CommandResult",
    "Database",
    "DatabaseInstance",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "LifecycleResult",
    "Order",
    "OrderDirection",
]
