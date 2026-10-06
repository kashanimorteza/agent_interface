"""The Database Interface: the only public entry point.

It declares behaviour and forwards it. Core validates and routes every request, and one Engine
unit does the storage work. Nothing else of the Database is published.
"""

from collections.abc import Mapping as _Mapping
from collections.abc import Sequence as _Sequence
from typing import Any as _Any

from database.core.data import Data as _Data
from database.core.errors import ConfigurationError as ConfigurationError
from database.core.errors import ConnectionFailureError as ConnectionFailureError
from database.core.errors import DatabaseError as DatabaseError
from database.core.errors import DeclarationMismatchError as DeclarationMismatchError
from database.core.errors import ExecutionError as ExecutionError
from database.core.errors import InactiveInstanceError as InactiveInstanceError
from database.core.errors import InvalidInputError as InvalidInputError
from database.core.errors import LifecycleError as LifecycleError
from database.core.initial_data import insert_initial_data as _insert_initial_data
from database.core.lifecycle import prepare as _prepare
from database.core.tables import create_tables as _create_tables
from database.core.values import CommandResult as CommandResult
from database.core.values import DatabaseInstance as DatabaseInstance
from database.core.values import Filter as Filter
from database.core.values import FilterCombination as FilterCombination
from database.core.values import FilterOperator as FilterOperator
from database.core.values import LifecycleResult as LifecycleResult
from database.core.values import Order as Order
from database.core.values import OrderDirection as OrderDirection


class Database:
    """One Database object offers every Operation and Lifecycle Command.

    Every call accepts an optional DatabaseInstance, last; without one the call runs on the
    configured default Instance.
    """

    def __init__(self) -> None:
        self._data = _Data()

    # ------------------------------------------------------------ Entity Operations
    def add(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        """Store one complete new Entity instance and return the stored Entity."""
        return self._data.add(entity, instance)

    def update(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        """Replace every mutable Field of the stored record; null when no record exists."""
        return self._data.update(entity, instance)

    def list(
        self,
        entity: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the Entities that match; a zero or negative limit means no limit."""
        return self._data.read(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: _Any, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Return the Entity with the given id, or null."""
        return self._data.get_by_id(entity, id, instance)

    def delete(self, entity: _Any, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Remove the record and return the final deleted Entity, or null."""
        return self._data.delete(entity, id, instance)

    def enable(self, entity: _Any, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Set only the activity Field to true and return the final Entity, or null."""
        return self._data.set_active(entity, id, True, instance)

    def disable(self, entity: _Any, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Set only the activity Field to false and return the final Entity, or null."""
        return self._data.set_active(entity, id, False, instance)

    def count(
        self,
        entity: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the total of a numeric Field, ignoring nulls, or zero."""
        return self._data.aggregate("sum", entity, field, filters, combination, instance)

    def min(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or null."""
        return self._data.aggregate("min", entity, field, filters, combination, instance)

    def max(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the largest value of a comparable Field, ignoring nulls, or null."""
        return self._data.aggregate("max", entity, field, filters, combination, instance)

    def truncate(self, entity: _Any, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._data.truncate(entity, instance)

    # ------------------------------------------------------------ Database-wide Operation
    def execute_command(
        self,
        command: str,
        parameters: _Mapping[str, _Any] | _Sequence[_Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Run a native command in the Instance Engine's query language."""
        return self._data.execute_command(command, parameters, instance)

    # ------------------------------------------------------------ Lifecycle Commands
    def create_tables(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Create every Table from the Model Entities; stop on a difference with an existing one."""
        return _create_tables(self._data, instance)

    def insert_initial_data(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Insert every missing configured Initial Data record; skip identical present ones."""
        return _insert_initial_data(self._data, instance)

    def prepare(self, instance: DatabaseInstance | None = None) -> LifecycleResult:
        """Run create_tables and then insert_initial_data; stop if create_tables fails."""
        return _prepare(self._data, instance)
