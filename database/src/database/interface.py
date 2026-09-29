"""Interface: the only public Database surface."""

import argparse
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from database.core.config import load_configuration as _load_configuration
from database.core.data import Data as _Data
from database.core.vocabulary import (
    CommandResult,
    DatabaseInstance,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)

__all__ = [
    "CommandResult",
    "Database",
    "DatabaseInstance",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "Order",
    "OrderDirection",
    "create_tables",
    "insert_initial_data",
    "main",
]


class Database:
    """Store, retrieve, and operate on Entity data in an active Instance.

    Every Operation accepts an optional Instance; the configured default Instance is used
    when it is omitted.
    """

    def __init__(self, configuration: Path | None = None) -> None:
        """Create the access surface.

        Args:
            configuration (Path, optional): Configuration file to use instead of the packaged one.
        """
        self._data = _Data(
            None if configuration is None else _load_configuration(configuration)
        )

    def add(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Persist a complete Entity instance and return it with generated values."""
        return self._data.add(entity, instance)

    def update(self, entity: Any, instance: DatabaseInstance | None = None) -> Any:
        """Replace every mutable Field of the record with the Entity's id; return None when absent."""
        return self._data.update(entity, instance)

    def list(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Sequence[Any]:
        """Return matching Entity instances; a limit of zero or less means no limit."""
        return self._data.list(entity, filters, combination, orders, limit, instance)

    def delete(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> bool:
        """Delete a record and report whether one existed."""
        return self._data.delete(entity, record_id, instance)

    def enable(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Set a record active and return it, or None when no record has the id."""
        return self._data.enable(entity, record_id, instance)

    def disable(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Set a record inactive and return it, or None when no record has the id."""
        return self._data.disable(entity, record_id, instance)

    def get_by_id(
        self, entity: Any, record_id: int, instance: DatabaseInstance | None = None
    ) -> Any:
        """Return the record with the id as an Entity instance, or None."""
        return self._data.get_by_id(entity, record_id, instance)

    def count(
        self,
        entity: Any,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> int:
        """Return the number of matching records."""
        return self._data.count(entity, filters, combination, instance)

    def sum(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the total of a numeric Field over matching records, ignoring null."""
        return self._data.sum(entity, field, filters, combination, instance)

    def min(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the smallest non-null value of a Field over matching records."""
        return self._data.min(entity, field, filters, combination, instance)

    def max(
        self,
        entity: Any,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        instance: DatabaseInstance | None = None,
    ) -> Any:
        """Return the largest non-null value of a Field over matching records."""
        return self._data.max(entity, field, filters, combination, instance)

    def truncate(self, entity: Any, instance: DatabaseInstance | None = None) -> int:
        """Remove every record of an Entity and return how many were removed."""
        return self._data.truncate(entity, instance)

    def execute_command(
        self,
        command: str,
        parameters: Mapping[str, Any] | None = None,
        instance: DatabaseInstance | None = None,
    ) -> CommandResult:
        """Execute a SQL command with named bound parameters."""
        return self._data.execute_command(command, parameters, instance)

    def create_tables(self, instance: DatabaseInstance | None = None) -> None:
        """Create or migrate every stored structure the Model Entities declare."""
        self._data.create_tables(instance)

    def insert_initial_data(self, instance: DatabaseInstance | None = None) -> int:
        """Insert the declared Initial Data the Instance does not hold; return the count."""
        return self._data.insert_initial_data(instance)


def create_tables(instance: DatabaseInstance | None = None) -> None:
    """Create or migrate every stored structure on an Instance.

    Args:
        instance (DatabaseInstance, optional): Instance to prepare; the default when omitted.
    """
    Database().create_tables(instance)


def insert_initial_data(instance: DatabaseInstance | None = None) -> int:
    """Insert the declared Initial Data into an Instance once its Tables exist.

    Args:
        instance (DatabaseInstance, optional): Instance to fill; the default when omitted.

    Returns:
        (int): Number of records inserted.
    """
    return Database().insert_initial_data(instance)


def main(argv: Sequence[str] | None = None) -> None:
    """Run Create Tables or Insert Initial Data as a manual command."""
    parser = argparse.ArgumentParser(prog="database")
    parser.add_argument("command", choices=("create-tables", "insert-initial-data"))
    parser.add_argument(
        "--instance", choices=[member.value for member in DatabaseInstance]
    )
    arguments = parser.parse_args(argv)
    instance = (
        None if arguments.instance is None else DatabaseInstance(arguments.instance)
    )
    if arguments.command == "create-tables":
        create_tables(instance)
        print("Tables are ready")
    else:
        print(f"Inserted {insert_initial_data(instance)} records")


if __name__ == "__main__":
    main()
