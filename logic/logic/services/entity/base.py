"""Base: the one shared structure that holds every Entity Action."""

import builtins as _builtins
from collections.abc import Sequence
from typing import Any, ClassVar

from logic.services.storage.interface import (
    Storage,
    database_error,
    database_instance,
    database_value,
)

_List = _builtins.list


class BaseEntity:
    """Holds one Storage access and every Action that every Child Service inherits."""

    _entity: ClassVar[type[Any]]

    def __init__(self) -> None:
        self._storage = Storage()

    def add(
        self,
        entity: Any,
        instance: database_instance | None = None,
    ) -> Any:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        if not isinstance(entity, self._entity):
            raise database_error.InvalidInputError(
                f"The entity must be an instance of {self._entity.__name__}"
            )
        return self._storage.add(entity, instance)

    def update(
        self,
        entity: Any,
        instance: database_instance | None = None,
    ) -> Any:
        """Replace every mutable Field of the stored record; its id only locates the record. Returns the stored Entity, or None."""
        if not isinstance(entity, self._entity):
            raise database_error.InvalidInputError(
                f"The entity must be an instance of {self._entity.__name__}"
            )
        return self._storage.update(entity, instance)

    def list(
        self,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        orders: Sequence[database_value.Order] | None = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> _List[Any]:
        """Return the matching Entities; a zero or negative limit means no limit."""
        return self._storage.list(
            self._entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the Entity with the id, or None when no record exists."""
        return self._storage.get_by_id(self._entity, id, instance)

    def delete(
        self,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Remove the record and return the final deleted Entity, or None when no record exists."""
        return self._storage.delete(self._entity, id, instance)

    def enable(
        self,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Set only is_active to true and return the final Entity, or None when no record exists."""
        return self._storage.enable(self._entity, id, instance)

    def disable(
        self,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Set only is_active to false and return the final Entity, or None when no record exists."""
        return self._storage.disable(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """Return the number of matching Entities."""
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls, or zero when nothing matches."""
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return self._storage.max(self._entity, field, filters, combination, instance)

    def truncate(
        self,
        instance: database_instance | None = None,
    ) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._storage.truncate(self._entity, instance)
