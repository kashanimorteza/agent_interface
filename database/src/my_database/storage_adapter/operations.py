"""Physical persistence operations over an Engine.

Every public method runs in its own short-lived transaction that is committed
or rolled back and closed before returning. Engine and driver failures are
translated into Database errors here; nothing else in the package touches the
driver.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator

from sqlalchemy import Table, delete, insert, select, text, update
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..errors import ConstraintError, DatabaseError, StatementError


class Storage:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    @contextmanager
    def transaction(self) -> Iterator[Connection]:
        try:
            with self._engine.begin() as connection:
                yield connection
        except DatabaseError:
            raise
        except IntegrityError as error:
            raise ConstraintError(_reason(error)) from None
        except SQLAlchemyError as error:
            raise StatementError(_reason(error)) from None

    def insert(self, table: Table, values: dict[str, Any]) -> int:
        with self.transaction() as connection:
            result = connection.execute(insert(table).values(**values))
            return int(result.inserted_primary_key[0])

    def select_one(self, table: Table, key: int) -> dict[str, Any] | None:
        with self.transaction() as connection:
            row = connection.execute(select(table).where(table.c.id == key)).mappings().first()
            return dict(row) if row is not None else None

    def select_many(
        self,
        table: Table,
        criteria: dict[str, Any],
        order_by: str,
        limit: int | None,
        offset: int | None,
    ) -> list[dict[str, Any]]:
        statement = select(table)
        for column, value in criteria.items():
            statement = statement.where(table.c[column] == value)
        statement = statement.order_by(table.c[order_by], table.c.id)
        if limit is not None:
            statement = statement.limit(limit)
        if offset is not None:
            statement = statement.offset(offset)
        with self.transaction() as connection:
            return [dict(row) for row in connection.execute(statement).mappings()]

    def update(self, table: Table, key: int, values: dict[str, Any]) -> int:
        with self.transaction() as connection:
            return connection.execute(update(table).where(table.c.id == key).values(**values)).rowcount

    def delete(self, table: Table, key: int) -> int:
        with self.transaction() as connection:
            return connection.execute(delete(table).where(table.c.id == key)).rowcount

    def execute(self, statement: str, parameters: dict[str, Any] | None) -> list[tuple[Any, ...]]:
        with self.transaction() as connection:
            result = connection.execute(text(statement), parameters or {})
            return [tuple(row) for row in result] if result.returns_rows else []


def _reason(error: SQLAlchemyError) -> str:
    origin = getattr(error, "orig", None)
    return str(origin) if origin is not None else str(error)
