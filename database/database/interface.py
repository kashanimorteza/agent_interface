"""The Database Interface: the only public entry point, published as six groups."""

import builtins
from collections.abc import Mapping, Sequence
from typing import Any

from database.core import data, errors, values
from database.core.initial_data import insert_initial_data
from database.core.setup import prepare
from database.core.tables import create_tables
from database.core.values import database_instance

__all__ = [
    "database_error",
    "database_instance",
    "database_interface",
    "database_result",
    "database_setup",
    "database_value",
]

type _Filters = Sequence[values.Filter] | None
type _Orders = Sequence[values.Order] | None


class database_interface:
    """Every Entity Operation and the Command Operation."""

    def add[E](self, entity: E, instance: database_instance | None = None) -> E:
        """Add one complete new Entity and return it as stored, with generated values."""
        return data.add(entity, instance)

    def update[E](
        self, entity: E, instance: database_instance | None = None
    ) -> E | None:
        """Replace every mutable Field of the record the Entity's id locates."""
        return data.update(entity, instance)

    def list[E](
        self,
        entity: type[E],
        filters: _Filters = None,
        combination: values.FilterCombination | None = None,
        orders: _Orders = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> builtins.list[E]:
        """The matching Entities in order, bounded by a positive limit."""
        return data.list_entities(entity, filters, combination, orders, limit, instance)

    def get_by_id[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """The Entity with the given id, or None."""
        return data.get_by_id(entity, id, instance)

    def delete[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Delete the Entity with the given id and return it, or None."""
        return data.delete(entity, id, instance)

    def enable[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Set only is_active to true and return the Entity, or None."""
        return data.set_activity(entity, id, True, instance)

    def disable[E](
        self, entity: type[E], id: int, instance: database_instance | None = None
    ) -> E | None:
        """Set only is_active to false and return the Entity, or None."""
        return data.set_activity(entity, id, False, instance)

    def count(
        self,
        entity: type,
        filters: _Filters = None,
        combination: values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """The number of matching Entities."""
        return data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: type,
        field: Any,
        filters: _Filters = None,
        combination: values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """The total of a numeric Field over matching Entities, or zero; nulls ignored."""
        return data.aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: type,
        field: Any,
        filters: _Filters = None,
        combination: values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """The smallest value of a Field over matching Entities, or None; nulls ignored."""
        return data.aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: type,
        field: Any,
        filters: _Filters = None,
        combination: values.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """The largest value of a Field over matching Entities, or None; nulls ignored."""
        return data.aggregate("max", entity, field, filters, combination, instance)

    def truncate(self, entity: type, instance: database_instance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the count."""
        return data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: database_instance | None = None,
    ) -> values.CommandResult:
        """Run one native command of the Instance Engine with bound parameters."""
        return data.execute_command(command, parameters, instance)


class database_setup:
    """Every Setup Operation."""

    def create_tables(
        self, instance: database_instance | None = None
    ) -> values.SetupResult:
        """Create every Table from the Model Entities; stop on any difference."""
        return create_tables(instance)

    def insert_initial_data(
        self, instance: database_instance | None = None
    ) -> values.SetupResult:
        """Insert every missing configured Initial Data record; fail on a conflict."""
        return insert_initial_data(instance)

    def prepare(self, instance: database_instance | None = None) -> values.SetupResult:
        """Run create_tables and then insert_initial_data."""
        return prepare(instance)


class database_value:
    """What a consumer passes: the values of Condition and Sort."""

    Filter = values.Filter
    FilterOperator = values.FilterOperator
    FilterCombination = values.FilterCombination
    Order = values.Order
    OrderDirection = values.OrderDirection


class database_result:
    """What a consumer reads back."""

    CommandResult = values.CommandResult
    SetupResult = values.SetupResult


class database_error:
    """Every Database error."""

    DatabaseError = errors.DatabaseError
    ConfigurationError = errors.ConfigurationError
    InactiveInstanceError = errors.InactiveInstanceError
    InvalidInputError = errors.InvalidInputError
    DeclarationMismatchError = errors.DeclarationMismatchError
    ConnectionFailureError = errors.ConnectionFailureError
    ExecutionError = errors.ExecutionError
    SetupError = errors.SetupError
