"""Data Access over the Database Interface.

Translates Logic's data operations into calls on ``trading_database.Database`` and Database errors into
Backend errors. Contains no application Behaviour and never reaches the engine, tables, or migrations.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from trading_database import (
    ConstraintViolationError,
    Database,
    DatabaseError,
    InvalidActionError,
    RecordNotFoundError,
    UnknownFieldError,
    UnknownModelError as DatabaseUnknownModelError,
    UnsupportedOperationError,
)

from trading_backend.errors import (
    BackendError,
    ConflictError,
    InvalidFieldError,
    NotFoundError,
    UnknownModelError,
    UnsupportedActionError,
)


def _translate(exc: DatabaseError) -> BackendError:
    if isinstance(exc, RecordNotFoundError):
        return NotFoundError(str(exc))
    if isinstance(exc, ConstraintViolationError):
        return ConflictError(str(exc))
    if isinstance(exc, UnknownFieldError):
        return InvalidFieldError(str(exc))
    if isinstance(exc, DatabaseUnknownModelError):
        return UnknownModelError(str(exc))
    if isinstance(exc, (InvalidActionError, UnsupportedOperationError)):
        return UnsupportedActionError(str(exc))
    return BackendError(str(exc))


class DataAccess:
    """Logical data operations for every shared Model, backed by one Database Interface instance."""

    def __init__(self, database: Database | None = None) -> None:
        self._database = database if database is not None else Database()

    def create(self, model: str, data: Mapping[str, Any]) -> dict[str, Any]:
        try:
            return self._database.create(model, data)
        except DatabaseError as exc:
            raise _translate(exc) from None

    def read(self, model: str, record_id: Any) -> dict[str, Any] | None:
        try:
            return self._database.read(model, record_id)
        except DatabaseError as exc:
            raise _translate(exc) from None

    def list(
        self,
        model: str,
        *,
        filters: Mapping[str, Any] | None = None,
        order_by: Sequence[str] | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        try:
            return self._database.list(model, filters=filters, order_by=order_by, limit=limit, offset=offset)
        except DatabaseError as exc:
            raise _translate(exc) from None

    def update(self, model: str, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
        try:
            return self._database.update(model, record_id, data)
        except DatabaseError as exc:
            raise _translate(exc) from None

    def delete(self, model: str, record_id: Any) -> None:
        try:
            self._database.delete(model, record_id)
        except DatabaseError as exc:
            raise _translate(exc) from None

    def set_status(self, model: str, record_id: Any, action: str) -> dict[str, Any]:
        try:
            return self._database.status(model, record_id, action)
        except DatabaseError as exc:
            raise _translate(exc) from None


_data_access: DataAccess | None = None


def get_data_access() -> DataAccess:
    """The application's DataAccess, created lazily from the settings-driven Database."""
    global _data_access
    if _data_access is None:
        _data_access = DataAccess()
    return _data_access


def reset_data_access() -> None:
    """Forget the cached DataAccess so the next call builds a fresh one (verification use)."""
    global _data_access
    _data_access = None
