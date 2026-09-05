"""The generic Database Interface facade.

A caller names a Model by its key, selects an operation, and supplies the data
or criteria that operation requires. Each call owns one transaction: it opens a
session from the private factory, delegates to the Data Logic pipeline, commits
on success, rolls back on error, and closes the session. The engine,
connection, session, and mapped classes are never exposed.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Iterator, Mapping

from ta_database.data_logic import pipeline


class DatabaseInterface:
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    @contextmanager
    def _session(self) -> Iterator[Any]:
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except BaseException:
            session.rollback()
            raise
        finally:
            session.close()

    def create(self, model: str, data: Mapping[str, Any]) -> dict[str, Any]:
        with self._session() as session:
            return pipeline.create(session, model, data)

    def read(self, model: str, record_id: Any) -> dict[str, Any] | None:
        with self._session() as session:
            return pipeline.read(session, model, record_id)

    def list(self, model: str, filters: Mapping[str, Any] | None = None, order_by: str | None = None,
             limit: int | None = None, offset: int | None = None) -> list[dict[str, Any]]:
        with self._session() as session:
            return pipeline.list_records(session, model, filters=filters, order_by=order_by, limit=limit, offset=offset)

    def update(self, model: str, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
        with self._session() as session:
            return pipeline.update(session, model, record_id, data)

    def delete(self, model: str, record_id: Any) -> None:
        with self._session() as session:
            pipeline.delete(session, model, record_id)

    def status(self, model: str, record_id: Any, action: str) -> dict[str, Any]:
        with self._session() as session:
            return pipeline.status(session, model, record_id, action)

    def execute_sql(self, command: str, params: Mapping[str, Any] | None = None) -> list[dict[str, Any]] | int:
        with self._session() as session:
            return pipeline.execute_sql(session, command, params)
