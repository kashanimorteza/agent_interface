from collections.abc import Mapping, Sequence
from enum import Enum
from typing import Any

from database.interface import CommandResult, Database, Filter, FilterCombination, LifecycleResult, Order


class Storage:
    def __init__(self) -> None:
        self._database = Database()

    def add(self, entity: Any, instance: Enum | None = None) -> Any:
        return self._database.add(entity, instance)

    def update(self, entity: Any, instance: Enum | None = None) -> Any:
        return self._database.update(entity, instance)

    def list(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: Enum | None = None,
    ) -> Sequence[Any]:
        return self._database.list(entity, filters, combination, orders, limit, instance)

    def get_by_id(self, entity: Any, id: int, instance: Enum | None = None) -> Any:
        return self._database.get_by_id(entity, id, instance)

    def delete(self, entity: Any, id: int, instance: Enum | None = None) -> Any:
        return self._database.delete(entity, id, instance)

    def enable(self, entity: Any, id: int, instance: Enum | None = None) -> Any:
        return self._database.enable(entity, id, instance)

    def disable(self, entity: Any, id: int, instance: Enum | None = None) -> Any:
        return self._database.disable(entity, id, instance)

    def count(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> int:
        return self._database.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._database.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._database.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._database.max(entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: Enum | None = None) -> int:
        return self._database.truncate(entity, instance)

    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | Sequence[Any] | None = None, instance: Enum | None = None
    ) -> CommandResult:
        return self._database.execute_command(command, parameters, instance)

    def create_tables(self, instance: Enum | None = None) -> LifecycleResult:
        return self._database.create_tables(instance)

    def insert_initial_data(self, instance: Enum | None = None) -> LifecycleResult:
        return self._database.insert_initial_data(instance)

    def prepare(self, instance: Enum | None = None) -> LifecycleResult:
        return self._database.prepare(instance)
