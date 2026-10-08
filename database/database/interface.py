"""The Database Interface: the only public boundary, publishing exactly six prefixed groups."""

from collections.abc import Sequence as _Sequence
from typing import Any as _Any

from database.core import configuration as _configuration
from database.core import errors as _errors
from database.core import values as _values
from database.core.data import Data as _Data
from database.core.setup import Setup as _Setup


class database_interface:
    """Every Entity Operation and the Command Operation; every Operation ends with the optional instance."""

    def __init__(self) -> None:
        self._data = _Data()

    def add(self, entity: _Any, instance: _Any = None) -> _Any:
        """Store one new Entity instance and return the stored Entity, including generated values."""
        return self._data.add(entity, instance)

    def update(self, entity: _Any, instance: _Any = None) -> _Any:
        """Replace every mutable Field of the stored record of an Entity instance; None when it does not exist."""
        return self._data.update(entity, instance)

    def list(
        self,
        entity: _Any,
        filters: _Any = None,
        combination: _Any = None,
        orders: _Any = None,
        limit: _Any = None,
        instance: _Any = None,
    ) -> _Sequence[_Any]:
        """Return the matching Entity instances; a zero or negative limit means no limit."""
        return self._data.list(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        """Return the Entity with that id, or None when no record exists."""
        return self._data.get_by_id(entity, id, instance)

    def delete(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        """Remove the record and return the deleted Entity, or None when no record exists."""
        return self._data.delete(entity, id, instance)

    def enable(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        """Set only is_active to true and return the final Entity, or None when no record exists."""
        return self._data.enable(entity, id, instance)

    def disable(self, entity: _Any, id: _Any, instance: _Any = None) -> _Any:
        """Set only is_active to false and return the final Entity, or None when no record exists."""
        return self._data.disable(entity, id, instance)

    def count(
        self,
        entity: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> int:
        """Return the number of matching records."""
        return self._data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        """Return the total of a numeric Field, ignoring null values, or zero when nothing matches."""
        return self._data.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        """Return the smallest non-null value of a comparable Field, or None when nothing matches."""
        return self._data.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: _Any,
        field: _Any,
        filters: _Any = None,
        combination: _Any = None,
        instance: _Any = None,
    ) -> _Any:
        """Return the largest non-null value of a comparable Field, or None when nothing matches."""
        return self._data.max(entity, field, filters, combination, instance)

    def truncate(self, entity: _Any, instance: _Any = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._data.truncate(entity, instance)

    def execute_command(
        self, command: _Any, parameters: _Any = None, instance: _Any = None
    ) -> _values.CommandResult:
        """Run a native command in the Instance Engine's query language with bound parameters."""
        return self._data.execute_command(command, parameters, instance)


class database_setup:
    """Every Setup Operation; each takes only the optional instance and returns a SetupResult."""

    def __init__(self) -> None:
        self._setup = _Setup()

    def create_tables(self, instance: _Any = None) -> _values.SetupResult:
        """Create the Tables of the Model Entity Collection; stop on a difference with an existing Table."""
        return self._setup.create_tables(instance)

    def insert_initial_data(self, instance: _Any = None) -> _values.SetupResult:
        """Insert every missing configured Initial Data record; skip identical ones; fail on conflicting ones."""
        return self._setup.insert_initial_data(instance)

    def prepare(self, instance: _Any = None) -> _values.SetupResult:
        """Run create_tables and then insert_initial_data; stop when create_tables fails."""
        return self._setup.prepare(instance)


class database_value:
    """What a consumer passes to an Operation: the Filter and Order values and their vocabulary."""

    Filter = _values.Filter
    FilterOperator = _values.FilterOperator
    FilterCombination = _values.FilterCombination
    Order = _values.Order
    OrderDirection = _values.OrderDirection


database_instance = _configuration.database_instance


class database_result:
    """What a consumer reads back from a Command or Setup Operation."""

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
