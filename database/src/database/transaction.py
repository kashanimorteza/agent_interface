"""The explicit Transaction boundary (Database Principle 14): a consumer groups related data
operations on one Instance into one atomic unit; a standalone write forms its own atomic unit."""

from __future__ import annotations

import sqlalchemy.orm as sa_orm

from database import observability
from database.adapter import StorageAdapter


class Transaction:
    """One unit of data operations on a single Instance whose changes commit together or roll
    back together (Database Principle 14). Database owns commit, rollback, and cleanup without
    exposing the underlying connection."""

    def __init__(self, adapter: StorageAdapter, instance_key: str | None = None) -> None:
        self._adapter = adapter
        self._instance_key = instance_key
        self._session: sa_orm.Session | None = None

    def __enter__(self) -> Transaction:
        self._session = self._adapter.new_session(self._instance_key)
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> bool:
        assert self._session is not None
        try:
            if exc_type is None:
                self._session.commit()
            else:
                self._session.rollback()
                observability.record_event(
                    "transaction_conflict" if exc_type is Exception else "transaction_rollback",
                    f"Transaction on Instance '{self._instance_key or '<default>'}' rolled back "
                    f"due to {getattr(exc_type, '__name__', exc_type)}.",
                )
        finally:
            self._session.close()
            self._session = None
        return False

    @property
    def session(self) -> sa_orm.Session:
        if self._session is None:
            raise RuntimeError("Transaction is not active; use it as a context manager.")
        return self._session
