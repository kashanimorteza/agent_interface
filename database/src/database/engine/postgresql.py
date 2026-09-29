"""Implementation of every Database Operation for the PostgreSQL Instance."""

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.types import TypeEngine

from database.core import migration, statements, structure
from database.core.config import EngineConfig, InstanceConfig
from database.core.vocabulary import (
    CommandResult,
    Filter,
    FilterCombination,
    Order,
)


def _decimal(precision: int | None, scale: int | None) -> TypeEngine[Any]:
    return sa.Numeric(precision, scale)


class PostgresqlInstance:
    """Storage and every Database Operation for one PostgreSQL Instance."""

    def __init__(
        self,
        instance: InstanceConfig,
        engine: EngineConfig,
        entities: Sequence[Any],
    ) -> None:
        self.engine = sa.create_engine(
            sa.URL.create(
                "postgresql+psycopg",
                username=instance.username or None,
                password=instance.password or None,
                host=instance.host or None,
                port=int(instance.port) if instance.port else None,
                database=instance.database,
            )
        )
        self.tables = self._metadata(entities).tables
        self.by_entity = {
            entity.declaration.name: self.tables[
                structure.table_name(entity.declaration.name)
            ]
            for entity in entities
        }

    @staticmethod
    def _metadata(entities: Sequence[Any]) -> sa.MetaData:
        return structure.build_metadata(entities, _decimal)

    def _table(self, entity: Any) -> sa.Table:
        return self.by_entity[entity.declaration.name]

    def create_tables(self, entities: Sequence[Any]) -> None:
        """Create or migrate the stored structure of the given Entities."""
        with self.engine.begin() as connection:
            migration.migrate(connection, self._metadata(entities), batch=False)

    def add(self, entity: Any, values: dict[str, Any]) -> dict[str, Any]:
        """Insert one record and return it as stored."""
        with self.engine.begin() as connection:
            return statements.insert(connection, self._table(entity), values)

    def update(self, entity: Any, values: dict[str, Any]) -> dict[str, Any] | None:
        """Replace the mutable Fields of the located record."""
        with self.engine.begin() as connection:
            return statements.update(
                connection, self._table(entity), entity.declaration, values
            )

    def get(self, entity: Any, record_id: Any) -> dict[str, Any] | None:
        """Return the record with the given identity, or None."""
        with self.engine.begin() as connection:
            return statements.get(
                connection,
                self._table(entity),
                entity.declaration.primary_key,
                record_id,
            )

    def select(
        self,
        entity: Any,
        filters: Sequence[Filter],
        combination: FilterCombination,
        orders: Sequence[Order],
        limit: int,
    ) -> list[dict[str, Any]]:
        """Return matching records in the requested order."""
        with self.engine.begin() as connection:
            return statements.select(
                connection, self._table(entity), filters, combination, orders, limit
            )

    def delete(self, entity: Any, record_id: Any) -> bool:
        """Delete the record with the given identity."""
        with self.engine.begin() as connection:
            return statements.delete(
                connection,
                self._table(entity),
                entity.declaration.primary_key,
                record_id,
            )

    def set_active(
        self, entity: Any, record_id: Any, active: bool
    ) -> dict[str, Any] | None:
        """Set the activity Field of the record with the given identity."""
        with self.engine.begin() as connection:
            return statements.set_active(
                connection,
                self._table(entity),
                entity.declaration.primary_key,
                record_id,
                active,
            )

    def count(
        self, entity: Any, filters: Sequence[Filter], combination: FilterCombination
    ) -> int:
        """Return the number of matching records."""
        with self.engine.begin() as connection:
            return statements.count(
                connection, self._table(entity), filters, combination
            )

    def aggregate(
        self,
        entity: Any,
        function: str,
        field: Any,
        filters: Sequence[Filter],
        combination: FilterCombination,
    ) -> Any:
        """Return the total, smallest, or largest value of a Field."""
        with self.engine.begin() as connection:
            return statements.aggregate(
                connection, self._table(entity), function, field, filters, combination
            )

    def truncate(self, entity: Any) -> int:
        """Remove every record of an Entity."""
        with self.engine.begin() as connection:
            return statements.truncate(connection, self._table(entity))

    def execute(self, command: str, parameters: Mapping[str, Any]) -> CommandResult:
        """Execute a command with bound parameters."""
        with self.engine.begin() as connection:
            return statements.execute(connection, command, parameters)

    @contextmanager
    def transaction(self) -> Iterator[statements.Transaction]:
        """Open one atomic change that reads and inserts records."""
        with self.engine.begin() as connection:
            yield statements.Transaction(connection, self.by_entity)


def create(
    instance: InstanceConfig, engine: EngineConfig, entities: Sequence[Any]
) -> PostgresqlInstance:
    """Create the implementation of the PostgreSQL Instance."""
    return PostgresqlInstance(instance, engine, entities)
