"""Database Interface: the only public entry point; it declares every contract and forwards to Core.

Every helper import is private (underscore-named), so the public names of this module are exactly the contracts.
"""

import builtins as _builtins
from collections.abc import Mapping as _Mapping, Sequence as _Sequence
from enum import Enum as _Enum
from typing import Any as _Any, cast as _cast

from sqlmodel import SQLModel as _SQLModel

from database.core import (
    data as _data,
    initial_data as _initial_data,
    tables as _tables,
)
from database.core.data import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
)

__all__ = [
    "CommandResult",
    "ConfigurationError",
    "ConnectionFailureError",
    "Database",
    "DatabaseError",
    "DatabaseInstance",
    "DeclarationMismatchError",
    "ExecutionError",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "InactiveInstanceError",
    "InvalidInputError",
    "LifecycleError",
    "LifecycleResult",
    "Order",
    "OrderDirection",
]


class Database:
    """The one object a consumer creates; every Operation and Lifecycle Command is called on it.

    Every call accepts an optional DatabaseInstance as its last parameter and runs on the configured default
    Instance when none is given. Creating a Database opens no connection.
    """

    def add[E: _SQLModel](self, entity: E, instance: _Enum | None = None) -> E:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        return _cast("E", _data.add(entity, instance))

    def update[E: _SQLModel](
        self, entity: E, instance: _Enum | None = None
    ) -> E | None:
        """Replace every mutable Field of the record the Entity's id locates; null when there is none."""
        return _cast("E | None", _data.update(entity, instance))

    def list[E: _SQLModel](
        self,
        entity: type[E],
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _Sequence[Order] | None = None,
        limit: int | None = None,
        instance: _Enum | None = None,
    ) -> _builtins.list[E]:
        """The matching Entities, ordered and limited; a limit of zero or below means no limit."""
        return _cast(
            "_builtins.list[E]",
            _data.list_entities(entity, filters, combination, orders, limit, instance),
        )

    def get_by_id[E: _SQLModel](
        self, entity: type[E], id: int, instance: _Enum | None = None
    ) -> E | None:
        """The Entity with the given id, or null when there is none."""
        return _cast("E | None", _data.get_by_id(entity, id, instance))

    def delete[E: _SQLModel](
        self, entity: type[E], id: int, instance: _Enum | None = None
    ) -> E | None:
        """Remove the record with the given id and return it as it was; null when there is none."""
        return _cast("E | None", _data.delete(entity, id, instance))

    def enable[E: _SQLModel](
        self, entity: type[E], id: int, instance: _Enum | None = None
    ) -> E | None:
        """Set only the activity flag to active; the final Entity, or null when there is none."""
        return _cast("E | None", _data.enable(entity, id, instance))

    def disable[E: _SQLModel](
        self, entity: type[E], id: int, instance: _Enum | None = None
    ) -> E | None:
        """Set only the activity flag to inactive; the final Entity, or null when there is none."""
        return _cast("E | None", _data.disable(entity, id, instance))

    def count(
        self,
        entity: type[_SQLModel],
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _Enum | None = None,
    ) -> int:
        """The number of matching records."""
        return _data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type[_SQLModel],
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _Enum | None = None,
    ) -> _Any:
        """The total of one numeric Field, ignoring nulls; zero when nothing matches."""
        return _data.total(entity, field, filters, combination, instance)

    def min(
        self,
        entity: type[_SQLModel],
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _Enum | None = None,
    ) -> _Any:
        """The smallest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return _data.smallest(entity, field, filters, combination, instance)

    def max(
        self,
        entity: type[_SQLModel],
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _Enum | None = None,
    ) -> _Any:
        """The largest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return _data.largest(entity, field, filters, combination, instance)

    def truncate(self, entity: type[_SQLModel], instance: _Enum | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the number removed."""
        return _data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: _Mapping[str, _Any] | _Sequence[_Any] | None = None,
        instance: _Enum | None = None,
    ) -> CommandResult:
        """Run one native command in the Instance Engine's query language with bound parameters."""
        return _data.execute_command(command, parameters, instance)

    def create_tables(self, instance: _Enum | None = None) -> LifecycleResult:
        """Create every Table of the Model's Entities; matching Tables are left unchanged."""
        return _tables.create_tables(instance)

    def insert_initial_data(self, instance: _Enum | None = None) -> LifecycleResult:
        """Insert every configured Initial Data record that is not already stored."""
        return _initial_data.insert_initial_data(instance)

    def prepare(self, instance: _Enum | None = None) -> LifecycleResult:
        """Run create_tables and then insert_initial_data; stop when create_tables fails."""
        return _initial_data.prepare(instance)
