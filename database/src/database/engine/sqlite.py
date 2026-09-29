"""Implementation of every Database Operation for the SQLite Instance."""

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from decimal import Decimal
from typing import Any

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.types import TypeEngine

from database.core import migration, statements, structure
from database.core.config import PACKAGE_ROOT, EngineConfig, InstanceConfig
from database.core.vocabulary import (
    CommandResult,
    Filter,
    FilterCombination,
    Order,
)


class _Untyped(sa.types.UserDefinedType[Any]):
    """Column without a type affinity, so SQLite keeps each value as supplied."""

    cache_ok = True

    def get_col_spec(self, **kw: Any) -> str:
        return "BLOB"


class ExactDecimal(sa.types.TypeDecorator[Decimal]):
    """Decimal stored as a number when that is exact and as text otherwise."""

    impl = _Untyped
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: sa.Dialect) -> float | str | None:
        if value is None:
            return None
        exact = value if isinstance(value, Decimal) else Decimal(str(value))
        approximate = float(exact)
        return approximate if Decimal(repr(approximate)) == exact else str(exact)

    def process_result_value(self, value: Any, dialect: sa.Dialect) -> Decimal | None:
        return (
            None
            if value is None
            else Decimal(value if isinstance(value, str) else repr(value))
        )


def _decimal(precision: int | None, scale: int | None) -> TypeEngine[Any]:
    if precision is not None or scale is not None:
        raise ValueError(
            "decimal precision and scale cannot be realized in SQLite storage"
        )
    return ExactDecimal()


class SqliteInstance:
    """Storage and every Database Operation for one SQLite Instance."""

    def __init__(
        self,
        instance: InstanceConfig,
        engine: EngineConfig,
        entities: Sequence[Any],
    ) -> None:
        path = PACKAGE_ROOT / instance.path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = sa.create_engine(
            f"sqlite:///{path}",
            connect_args={"check_same_thread": engine.parameters["check_same_thread"]},
        )
        foreign_keys = engine.parameters["foreign_keys"]

        @event.listens_for(self.engine, "connect")
        def _connect(connection: Any, record: Any) -> None:
            connection.isolation_level = None
            connection.execute(f"PRAGMA foreign_keys={'ON' if foreign_keys else 'OFF'}")

        @event.listens_for(self.engine, "begin")
        def _begin(connection: sa.Connection) -> None:
            connection.exec_driver_sql("BEGIN")

        self.tables = self._metadata(entities).tables
        self.by_entity = {
            entity.declaration.name: self.tables[
                structure.table_name(entity.declaration.name)
            ]
            for entity in entities
        }

    @staticmethod
    def _metadata(entities: Sequence[Any]) -> sa.MetaData:
        return structure.build_metadata(
            entities, _decimal, {"sqlite_autoincrement": True}
        )

    def _table(self, entity: Any) -> sa.Table:
        return self.by_entity[entity.declaration.name]

    def create_tables(self, entities: Sequence[Any]) -> None:
        """Create or migrate the stored structure of the given Entities."""
        with self.engine.begin() as connection:
            migration.migrate(connection, self._metadata(entities), batch=True)

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
) -> SqliteInstance:
    """Create the implementation of the SQLite Instance."""
    return SqliteInstance(instance, engine, entities)
