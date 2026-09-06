"""The Database Interface — the only boundary published to consumers.

A caller names a Model (its key in .interface/config/model.yaml), an operation, and the data or
criteria the operation needs. The engine, connections, sessions, ORM classes, migrations, and the
database file never leave this class.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from my_database.data_logic import operations as _ops
from my_database.storage_adapter.engine import create_database_engine, session_factory


class Database:
    """Generic data access for every persistent Model plus controlled, parameterized SQL execution."""

    def __init__(self, url: str | None = None) -> None:
        self._engine = create_database_engine(url)
        self._sessions = session_factory(self._engine)

    @contextmanager
    def _transaction(self) -> Iterator[Session]:
        with self._sessions() as session, session.begin():
            yield session

    # ------------------------------------------------------------ Model operations

    def create(self, model: str, data: Mapping[str, Any]) -> dict[str, Any]:
        """Insert one record of ``model`` and return it (credential fields excluded)."""
        with self._transaction() as session:
            return _ops.create(session, model, data)

    def read(self, model: str, record_id: Any) -> dict[str, Any] | None:
        """One record by primary key, or None when absent."""
        with self._transaction() as session:
            return _ops.read(session, model, record_id)

    def list(
        self,
        model: str,
        *,
        filters: Mapping[str, Any] | None = None,
        order_by: Sequence[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """Records matching equality ``filters``, ordered by ``order_by`` (leading '-' = descending) and paged."""
        with self._transaction() as session:
            return _ops.list_records(session, model, filters=filters, order_by=order_by, limit=limit, offset=offset)

    def update(self, model: str, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
        """Apply a partial update to one record and return it."""
        with self._transaction() as session:
            return _ops.update(session, model, record_id, data)

    def delete(self, model: str, record_id: Any) -> None:
        """Remove one record, subject to RESTRICT referential actions."""
        with self._transaction() as session:
            _ops.delete(session, model, record_id)

    def status(self, model: str, record_id: Any, action: str) -> dict[str, Any]:
        """``enable`` or ``disable`` one record through its status field."""
        with self._transaction() as session:
            return _ops.set_status(session, model, record_id, action)

    # ------------------------------------------------------------ controlled SQL

    def execute_sql(
        self, statement: str, parameters: Mapping[str, Any] | Sequence[Mapping[str, Any]] | None = None
    ) -> list[dict[str, Any]] | int:
        """Execute one SQL statement with bound ``:name`` parameters inside a transaction.

        Returns the rows as dicts when the statement returns rows, otherwise the affected row count.
        Values are never interpolated into the statement text.
        """
        if not isinstance(statement, str):
            raise TypeError("statement must be a str; supply values through parameters")
        with self._engine.begin() as connection:
            result = connection.execute(text(statement), parameters if parameters is not None else {})
            if result.returns_rows:
                return [dict(row._mapping) for row in result]
            return result.rowcount
