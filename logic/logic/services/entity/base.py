from collections.abc import Sequence
from enum import Enum
from typing import Any, ClassVar

from logic.services.storage.interface import Filter, FilterCombination, InvalidInputError, Order, Storage


class BaseEntity:
    _entity: ClassVar[Any]

    def __init__(self) -> None:
        self._storage = Storage()

    def _check(self, entity: Any) -> None:
        if not isinstance(entity, self._entity):
            raise InvalidInputError(f"An instance of {self._entity.__name__} is required")

    def add(self, entity: Any, instance: Enum | None = None) -> Any:
        self._check(entity)
        return self._storage.add(entity, instance)

    def update(self, entity: Any, instance: Enum | None = None) -> Any:
        self._check(entity)
        return self._storage.update(entity, instance)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: Enum | None = None,
    ) -> Sequence[Any]:
        return self._storage.list(self._entity, filters, combination, orders, limit, instance)

    def get_by_id(self, id: int, instance: Enum | None = None) -> Any:
        return self._storage.get_by_id(self._entity, id, instance)

    def delete(self, id: int, instance: Enum | None = None) -> Any:
        return self._storage.delete(self._entity, id, instance)

    def enable(self, id: int, instance: Enum | None = None) -> Any:
        return self._storage.enable(self._entity, id, instance)

    def disable(self, id: int, instance: Enum | None = None) -> Any:
        return self._storage.disable(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> int:
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        return self._storage.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: Enum | None = None) -> int:
        return self._storage.truncate(self._entity, instance)
