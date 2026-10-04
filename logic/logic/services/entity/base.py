"""Entity Service Base: the one shared structure that offers every Action for a bound Entity."""

import builtins
from collections.abc import Sequence
from enum import Enum
from typing import Any

from sqlmodel import SQLModel

from logic.services.storage.interface import (
    Filter,
    FilterCombination,
    InvalidInputError,
    Order,
    Storage,
)


class BaseEntity[E: SQLModel]:
    """The one shared structure of Entity Service: every Child Service receives it and offers its Actions for one bound Entity.

    Creating one takes one Storage access and opens no connection; every Action uses that same access.
    """

    _entity: type[E]

    def __init__(self) -> None:
        self._storage = Storage()

    def add(self, entity: E, instance: Enum | None = None) -> E:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        if not isinstance(entity, self._entity):
            raise InvalidInputError(
                f"An instance of {self._entity.__name__} is required."
            )
        return self._storage.add(entity, instance)

    def update(self, entity: E, instance: Enum | None = None) -> E | None:
        """Replace every mutable Field of the record the Entity's id locates; null when there is none."""
        if not isinstance(entity, self._entity):
            raise InvalidInputError(
                f"An instance of {self._entity.__name__} is required."
            )
        return self._storage.update(entity, instance)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: Enum | None = None,
    ) -> builtins.list[E]:
        """The matching Entities, ordered and limited; a limit of zero or below means no limit."""
        return self._storage.list(
            self._entity, filters, combination, orders, limit, instance
        )

    def get_by_id(self, id: int, instance: Enum | None = None) -> E | None:
        """The Entity with the given id, or null when there is none."""
        return self._storage.get_by_id(self._entity, id, instance)

    def delete(self, id: int, instance: Enum | None = None) -> E | None:
        """Remove the record with the given id and return it as it was; null when there is none."""
        return self._storage.delete(self._entity, id, instance)

    def enable(self, id: int, instance: Enum | None = None) -> E | None:
        """Set only the activity flag to active; the final Entity, or null when there is none."""
        return self._storage.enable(self._entity, id, instance)

    def disable(self, id: int, instance: Enum | None = None) -> E | None:
        """Set only the activity flag to inactive; the final Entity, or null when there is none."""
        return self._storage.disable(self._entity, id, instance)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> int:
        """The number of matching records."""
        return self._storage.count(self._entity, filters, combination, instance)

    def sum(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The total of one numeric Field, ignoring nulls; zero when nothing matches."""
        return self._storage.sum(self._entity, field, filters, combination, instance)

    def min(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The smallest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return self._storage.min(self._entity, field, filters, combination, instance)

    def max(
        self,
        field: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: Enum | None = None,
    ) -> Any:
        """The largest value of one comparable Field, ignoring nulls; null when nothing matches."""
        return self._storage.max(self._entity, field, filters, combination, instance)

    def truncate(self, instance: Enum | None = None) -> int:
        """Remove every record of the Entity, keep its Table, and return the number removed."""
        return self._storage.truncate(self._entity, instance)
