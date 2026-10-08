"""Interface: the only public entry point of Database, published as six prefixed groups."""

import builtins as _builtins
from collections.abc import Mapping, Sequence
from typing import Any

from .core import data as _data
from .core import errors as _errors
from .core import setup as _setup
from .core import values as _values
from .core.values import database_instance

_List = _builtins.list


class database_interface:
    """Calls every Entity Operation and the Command Operation, on an optional Instance."""

    def add(self, entity: Any, instance: database_instance | None = None) -> Any:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        return _data.add(entity, instance)

    def update(self, entity: Any, instance: database_instance | None = None) -> Any:
        """Replace every mutable Field of the stored record; its id only locates the record. Returns the stored Entity, or None."""
        return _data.update(entity, instance)

    def list(
        self,
        entity: Any,
        filters: Sequence[_values.Filter] | None = None,
        combination: _values.FilterCombination | None = None,
        orders: Sequence[_values.Order] | None = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> _List[Any]:
        """Return the matching Entities; a zero or negative limit means no limit."""
        return _data.list_entities(
            entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self, entity: Any, id: int, instance: database_instance | None = None
    ) -> Any:
        """Return the Entity with the id, or None when no record exists."""
        return _data.get_by_id(entity, id, instance)

    def delete(
        self, entity: Any, id: int, instance: database_instance | None = None
    ) -> Any:
        """Remove the record and return the final deleted Entity, or None when no record exists."""
        return _data.delete(entity, id, instance)

    def enable(
        self, entity: Any, id: int, instance: database_instance | None = None
    ) -> Any:
        """Set only is_active to true and return the final Entity, or None when no record exists."""
        return _data.enable(entity, id, instance)

    def disable(
        self, entity: Any, id: int, instance: database_instance | None = None
    ) -> Any:
        """Set only is_active to false and return the final Entity, or None when no record exists."""
        return _data.disable(entity, id, instance)

    def count(
        self,
        entity: Any,
        filters: Sequence[_values.Filter] | None = None,
        combination: _values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """Return the number of matching Entities."""
        return _data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[_values.Filter] | None = None,
        combination: _values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls, or zero when nothing matches."""
        return _data.total(entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[_values.Filter] | None = None,
        combination: _values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return _data.smallest(entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[_values.Filter] | None = None,
        combination: _values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return _data.largest(entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: database_instance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return _data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: database_instance | None = None,
    ) -> _values.CommandResult:
        """Run a native command in the Instance Engine's query language with bound parameters."""
        return _data.execute_command(command, parameters, instance)


class database_setup:
    """Calls every Setup Operation, on an optional Instance."""

    def create_tables(
        self, instance: database_instance | None = None
    ) -> _values.SetupResult:
        """Create the Table of every Entity; matching Tables are left unchanged and a difference stops the command."""
        return _setup.create_tables(instance)

    def insert_initial_data(
        self, instance: database_instance | None = None
    ) -> _values.SetupResult:
        """Insert every missing Initial Data record, skip identical present records, and fail on a conflicting one."""
        return _setup.insert_initial_data(instance)

    def prepare(self, instance: database_instance | None = None) -> _values.SetupResult:
        """Run create_tables and then insert_initial_data; stop without inserting when create_tables fails."""
        return _setup.prepare(instance)


class database_value:
    """The values a consumer passes to an Operation."""

    Filter = _values.Filter
    FilterOperator = _values.FilterOperator
    FilterCombination = _values.FilterCombination
    Order = _values.Order
    OrderDirection = _values.OrderDirection


class database_result:
    """The Results a consumer reads back."""

    CommandResult = _values.CommandResult
    SetupResult = _values.SetupResult


class database_error:
    """Every Database error, so a consumer can catch it."""

    DatabaseError = _errors.DatabaseError
    ConfigurationError = _errors.ConfigurationError
    InactiveInstanceError = _errors.InactiveInstanceError
    InvalidInputError = _errors.InvalidInputError
    DeclarationMismatchError = _errors.DeclarationMismatchError
    ConnectionFailureError = _errors.ConnectionFailureError
    ExecutionError = _errors.ExecutionError
    SetupError = _errors.SetupError


__all__ = [
    "database_error",
    "database_instance",
    "database_interface",
    "database_result",
    "database_setup",
    "database_value",
]
