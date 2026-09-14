"""Backend's Database Interface (task P3-G2-T1): Logic's only route to persistence.

Translates every persistence request into a call on Database's Public Interface, groups
related operations under one Database Instance's Transaction boundary, and bounds every
call with a finite timeout and, for safe/idempotent operations, a bounded retry.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from contextlib import contextmanager
from typing import Any, TypeVar

from database import ConstraintViolation, Database, Transaction, TransactionConflict

ModelT = TypeVar("ModelT")


class PersistenceTimeout(Exception):
    """Raised when a persistence interaction exceeds its finite timeout."""


class DatabaseInterface:
    """Backend's translation boundary to Database's Public Interface."""

    def __init__(
        self,
        db: Database,
        *,
        timeout_seconds: float,
        max_retry_attempts: int,
    ) -> None:
        self._db = db
        self._timeout = timeout_seconds
        self._max_retry_attempts = max_retry_attempts
        self._executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="db-interface")

    def close(self) -> None:
        self._executor.shutdown(wait=True)

    def _call(
        self, fn: Callable[..., Any], *args: Any, retryable: bool = False, **kwargs: Any
    ) -> Any:
        attempts = max(self._max_retry_attempts if retryable else 1, 1)
        for attempt in range(attempts):
            future = self._executor.submit(fn, *args, **kwargs)
            try:
                return future.result(timeout=self._timeout)
            except FutureTimeoutError as exc:
                raise PersistenceTimeout(
                    "Persistence interaction exceeded its finite timeout"
                ) from exc
            except TransactionConflict:
                if attempt + 1 < attempts:
                    continue
                raise
        raise RuntimeError("unreachable: the loop above always returns or raises")

    def create(self, instance: Any, *, txn: Transaction | None = None) -> Any:
        return self._call(self._db.create, instance, txn=txn)

    def get(
        self, model_cls: type[ModelT], id_: int, *, txn: Transaction | None = None
    ) -> ModelT | None:
        return self._call(self._db.get, model_cls, id_, txn=txn)

    def list(
        self, model_cls: type[ModelT], *, txn: Transaction | None = None, **filters: Any
    ) -> tuple[ModelT, ...]:
        return self._call(self._db.list, model_cls, txn=txn, **filters)

    def update(self, instance: Any, *, txn: Transaction | None = None) -> Any:
        return self._call(self._db.update, instance, txn=txn, retryable=True)

    def delete(self, model_cls: type[Any], id_: int, *, txn: Transaction | None = None) -> None:
        self._call(self._db.delete, model_cls, id_, txn=txn)

    def activate(
        self, model_cls: type[ModelT], id_: int, *, enable: bool, txn: Transaction | None = None
    ) -> ModelT:
        return self._call(self._db.activate, model_cls, id_, enable=enable, txn=txn, retryable=True)

    def verify_credential(
        self, model_cls: type[Any], field_name: str, candidate: str
    ) -> int | None:
        return self._call(self._db.verify_credential, model_cls, field_name, candidate)

    @contextmanager
    def transaction(self) -> Iterator[Transaction]:
        with self._db.transaction() as txn:
            yield txn


__all__ = ["ConstraintViolation", "DatabaseInterface", "PersistenceTimeout", "Transaction"]
