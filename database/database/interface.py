import builtins as _builtins
from collections.abc import Mapping as _Mapping
from collections.abc import Sequence as _Sequence
from typing import Any as _Any
from database.core import data as _data
from database.core import lifecycle as _lifecycle

from database.core.errors import ConfigurationError as ConfigurationError
from database.core.errors import ConnectionFailureError as ConnectionFailureError
from database.core.errors import DatabaseError as DatabaseError
from database.core.errors import DeclarationMismatchError as DeclarationMismatchError
from database.core.errors import ExecutionError as ExecutionError
from database.core.errors import InactiveInstanceError as InactiveInstanceError
from database.core.errors import InvalidInputError as InvalidInputError
from database.core.errors import LifecycleError as LifecycleError

from database.core.values import CommandResult as CommandResult
from database.core.values import DatabaseInstance as DatabaseInstance
from database.core.values import Filter as Filter
from database.core.values import FilterCombination as FilterCombination
from database.core.values import FilterOperator as FilterOperator
from database.core.values import Order as Order
from database.core.values import OrderDirection as OrderDirection
from database.core.values import SetupResult as SetupResult


class Database:
    """Entity Operations on the stored data of every Model Entity."""

    def add(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.add(entity, instance)

    def update(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.update(entity, instance)

    def list(
        self,
        entity: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _builtins.list[_Any]:
        return _data.list_entities(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: _Any, id: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.get_by_id(entity, id, instance)

    def delete(self, entity: _Any, id: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.delete(entity, id, instance)

    def enable(self, entity: _Any, id: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.set_active(entity, id, True, instance)

    def disable(self, entity: _Any, id: _Any, instance: DatabaseInstance | None = None) -> _Any:
        return _data.set_active(entity, id, False, instance)

    def count(
        self,
        entity: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        return _data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        return _data.aggregate("sum_values", entity, field, filters, combination, instance)

    def min(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        return _data.aggregate("min_value", entity, field, filters, combination, instance)

    def max(
        self,
        entity: _Any,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        return _data.aggregate("max_value", entity, field, filters, combination, instance)

    def truncate(self, entity: _Any, instance: DatabaseInstance | None = None) -> int:
        return _data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: _Mapping[str, _Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        return _data.execute_command(command, parameters, instance)


class Setup:
    """Setup Operations that prepare the storage of an Instance."""

    def create_tables(self, instance: DatabaseInstance | None = None) -> SetupResult:
        return _lifecycle.create_tables(instance)

    def insert_initial_data(self, instance: DatabaseInstance | None = None) -> SetupResult:
        return _lifecycle.insert_initial_data(instance)

    def prepare(self, instance: DatabaseInstance | None = None) -> SetupResult:
        return _lifecycle.prepare(instance)
