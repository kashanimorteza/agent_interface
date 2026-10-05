import collections.abc as _abc
import enum as _enum
import typing as _typing

from database.core import data as _data
from database.core import initial_data as _initial_data
from database.core import tables as _tables
from database.core.data import CommandResult as CommandResult
from database.core.data import ConfigurationError as ConfigurationError
from database.core.data import ConnectionFailureError as ConnectionFailureError
from database.core.data import DatabaseError as DatabaseError
from database.core.data import DatabaseInstance as DatabaseInstance
from database.core.data import DeclarationMismatchError as DeclarationMismatchError
from database.core.data import ExecutionError as ExecutionError
from database.core.data import Filter as Filter
from database.core.data import FilterCombination as FilterCombination
from database.core.data import FilterOperator as FilterOperator
from database.core.data import InactiveInstanceError as InactiveInstanceError
from database.core.data import InvalidInputError as InvalidInputError
from database.core.data import LifecycleError as LifecycleError
from database.core.data import LifecycleResult as LifecycleResult
from database.core.data import Order as Order
from database.core.data import OrderDirection as OrderDirection


class Database:
    def add(self, entity: _typing.Any, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.add(entity, instance)

    def update(self, entity: _typing.Any, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.update(entity, instance)

    def list(
        self,
        entity: _typing.Any,
        filters: _abc.Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _abc.Sequence[Order] | None = None,
        limit: int | None = None,
        instance: _enum.Enum | None = None,
    ) -> _abc.Sequence[_typing.Any]:
        return _data.list_entities(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: _typing.Any, id: int, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.get_by_id(entity, id, instance)

    def delete(self, entity: _typing.Any, id: int, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.delete(entity, id, instance)

    def enable(self, entity: _typing.Any, id: int, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.enable(entity, id, instance)

    def disable(self, entity: _typing.Any, id: int, instance: _enum.Enum | None = None) -> _typing.Any:
        return _data.disable(entity, id, instance)

    def count(
        self,
        entity: _typing.Any,
        filters: _abc.Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _enum.Enum | None = None,
    ) -> int:
        return _data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: _typing.Any,
        field: _typing.Any,
        filters: _abc.Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _enum.Enum | None = None,
    ) -> _typing.Any:
        return _data.total(entity, field, filters, combination, instance)

    def min(
        self,
        entity: _typing.Any,
        field: _typing.Any,
        filters: _abc.Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _enum.Enum | None = None,
    ) -> _typing.Any:
        return _data.smallest(entity, field, filters, combination, instance)

    def max(
        self,
        entity: _typing.Any,
        field: _typing.Any,
        filters: _abc.Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: _enum.Enum | None = None,
    ) -> _typing.Any:
        return _data.largest(entity, field, filters, combination, instance)

    def truncate(self, entity: _typing.Any, instance: _enum.Enum | None = None) -> int:
        return _data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: _abc.Mapping[str, _typing.Any] | _abc.Sequence[_typing.Any] | None = None,
        instance: _enum.Enum | None = None,
    ) -> CommandResult:
        return _data.execute_command(command, parameters, instance)

    def create_tables(self, instance: _enum.Enum | None = None) -> LifecycleResult:
        return _tables.create_tables(instance)

    def insert_initial_data(self, instance: _enum.Enum | None = None) -> LifecycleResult:
        return _initial_data.insert_initial_data(instance)

    def prepare(self, instance: _enum.Enum | None = None) -> LifecycleResult:
        return _initial_data.prepare(instance)
