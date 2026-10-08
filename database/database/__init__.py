"""Interface: the six groups through which Database is used."""

from collections.abc import Sequence as _Sequence
from typing import Any as _Any

from database.core import configuration as _configuration
from database.core import data as _data
from database.core import errors as _errors
from database.core import setup as _setup
from database.core import values as _values

__all__ = [
    "database_error",
    "database_instance",
    "database_interface",
    "database_result",
    "database_setup",
    "database_value",
]


class database_interface:
    """Every Entity Operation and the Command Operation."""

    def add(self, entity: _Any, instance: _Any = None) -> _Any:
        return _data.add(entity, instance)

    def update(self, entity: _Any, instance: _Any = None) -> _Any:
        return _data.update(entity, instance)

    def list(
        self,
        entity: _Any,
        filters: _Any = None,
        combination: _Any = None,
        orders: _Any = None,
        limit: _Any = None,
        instance: _Any = None,
    ) -> _Sequence[_Any]:
        return _data.list_all(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        return _data.get_by_id(entity, id, instance)

    def delete(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        return _data.delete(entity, id, instance)

    def enable(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        return _data.set_active(entity, id, True, instance)

    def disable(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        return _data.set_active(entity, id, False, instance)

    def count(
        self,
        entity: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> int:
        return _data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        return _data.total(entity, field, filters, combination, instance)

    def min(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        return _data.extreme(entity, field, filters, combination, False, instance)

    def max(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        return _data.extreme(entity, field, filters, combination, True, instance)

    def truncate(self, entity: _Any, instance: _Any = None) -> int:
        return _data.truncate(entity, instance)

    def execute_command(
        self, command: _Any, parameters: _Any = None, instance: _Any = None
    ) -> _values.CommandResult:
        return _data.execute_command(command, parameters, instance)


class database_setup:
    """Every Setup Operation."""

    def create_tables(self, instance: _Any = None) -> _values.SetupResult:
        return _setup.create_tables(instance)

    def insert_initial_data(self, instance: _Any = None) -> _values.SetupResult:
        return _setup.insert_initial_data(instance)

    def prepare(self, instance: _Any = None) -> _values.SetupResult:
        return _setup.prepare(instance)


class database_value:
    """What a consumer passes to an Operation."""

    Filter = _values.Filter
    FilterOperator = _values.FilterOperator
    FilterCombination = _values.FilterCombination
    Order = _values.Order
    OrderDirection = _values.OrderDirection


database_instance = _configuration.instance_enum()
"""The active Instances; one member per active configured Instance."""


class database_result:
    """What a consumer reads back."""

    CommandResult = _values.CommandResult
    SetupResult = _values.SetupResult


class database_error:
    """Every Error, so a consumer can catch it."""

    DatabaseError = _errors.DatabaseError
    ConfigurationError = _errors.ConfigurationError
    InactiveInstanceError = _errors.InactiveInstanceError
    InvalidInputError = _errors.InvalidInputError
    DeclarationMismatchError = _errors.DeclarationMismatchError
    ConnectionFailureError = _errors.ConnectionFailureError
    ExecutionError = _errors.ExecutionError
    SetupError = _errors.SetupError
