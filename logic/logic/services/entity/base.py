"""Base: the one shared structure that offers every Action to every Child Service."""

from collections.abc import Sequence as _Sequence
from typing import Any as _Any

from logic.services.storage.interface import (
    DatabaseInstance,
    Filter,
    FilterCombination,
    InvalidInputError,
    Order,
    Storage,
)


class BaseEntity:
    """Every Action of an Entity Child Service, bound to one Entity and handed to Storage."""

    _entity: type[_Any]

    def __init__(self) -> None:
        self._storage = Storage()

    def _require_bound(self, entity: _Any) -> None:
        if not isinstance(entity, self._entity):
            raise InvalidInputError(f"Expected an instance of {self._entity.__name__}")

    def add(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        """Store one complete new Entity instance and return the stored Entity."""
        self._require_bound(entity)
        return self._storage.add(entity, instance)

    def update(self, entity: _Any, instance: DatabaseInstance | None = None) -> _Any:
        """Replace every mutable Field of the stored record; null when no record exists."""
        self._require_bound(entity)
        return self._storage.update(entity, instance)

    def list(
        self,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: _Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the Entities that match; a zero or negative limit means no limit."""
        return self._storage.list(self._entity, filters, combination, orders, limit, instance)

    def get_by_id(self, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Return the Entity with the given id, or null."""
        return self._storage.get_by_id(self._entity, id, instance)

    def delete(self, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Remove the record and return the final deleted Entity, or null."""
        return self._storage.delete(self._entity, id, instance)

    def enable(self, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Set only the activity Field to true and return the final Entity, or null."""
        return self._storage.enable(self._entity, id, instance)

    def disable(self, id: int, instance: DatabaseInstance | None = None) -> _Any:
        """Set only the activity Field to false and return the final Entity, or null."""
        return self._storage.disable(self._entity, id, instance)

    def count(
        self,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the total of a numeric Field, ignoring nulls, or zero."""
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or null."""
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: _Any,
        filters: _Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> _Any:
        """Return the largest value of a comparable Field, ignoring nulls, or null."""
        return self._storage.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._storage.truncate(self._entity, instance)
