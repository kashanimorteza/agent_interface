"""Core: the one Storage gateway to Database."""

import builtins as _builtins
from collections.abc import Mapping, Sequence
from typing import Any

from database import (
    database_instance,
    database_interface,
    database_result,
    database_value,
)

_List = _builtins.list


class Storage:
    """Logic's gateway to Database: one Action for every Operation of Database's Interface group."""

    def __init__(self) -> None:
        self._database = database_interface()

    def add(
        self,
        entity: Any,
        instance: database_instance | None = None,
    ) -> Any:
        """Store one complete new Entity and return the stored Entity, including generated values."""
        return self._database.add(entity, instance)

    def update(
        self,
        entity: Any,
        instance: database_instance | None = None,
    ) -> Any:
        """Replace every mutable Field of the stored record; its id only locates the record. Returns the stored Entity, or None."""
        return self._database.update(entity, instance)

    def list(
        self,
        entity: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        orders: Sequence[database_value.Order] | None = None,
        limit: int | None = None,
        instance: database_instance | None = None,
    ) -> _List[Any]:
        """Return the matching Entities; a zero or negative limit means no limit."""
        return self._database.list(
            entity, filters, combination, orders, limit, instance
        )

    def get_by_id(
        self,
        entity: Any,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the Entity with the id, or None when no record exists."""
        return self._database.get_by_id(entity, id, instance)

    def delete(
        self,
        entity: Any,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Remove the record and return the final deleted Entity, or None when no record exists."""
        return self._database.delete(entity, id, instance)

    def enable(
        self,
        entity: Any,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Set only is_active to true and return the final Entity, or None when no record exists."""
        return self._database.enable(entity, id, instance)

    def disable(
        self,
        entity: Any,
        id: int,
        instance: database_instance | None = None,
    ) -> Any:
        """Set only is_active to false and return the final Entity, or None when no record exists."""
        return self._database.disable(entity, id, instance)

    def count(
        self,
        entity: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> int:
        """Return the number of matching Entities."""
        return self._database.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the total of a numeric Field, ignoring nulls, or zero when nothing matches."""
        return self._database.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the smallest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return self._database.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: Any,
        filters: Sequence[database_value.Filter] | None = None,
        combination: database_value.FilterCombination | None = None,
        instance: database_instance | None = None,
    ) -> Any:
        """Return the largest value of a comparable Field, ignoring nulls, or None when nothing matches."""
        return self._database.max(entity, field, filters, combination, instance)

    def truncate(
        self,
        entity: Any,
        instance: database_instance | None = None,
    ) -> int:
        """Remove every record of the Entity, keep its Table, and return the deleted count."""
        return self._database.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | Sequence[Any] | None = None,
        instance: database_instance | None = None,
    ) -> database_result.CommandResult:
        """Run a native command in the Instance Engine's query language with bound parameters."""
        return self._database.execute_command(command, parameters, instance)
