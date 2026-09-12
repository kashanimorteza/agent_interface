"""Database Interface: Backend's only route to persistence.

Translates a Logic-requested persistence operation or related-operation
group into the generic public interface published by Database, and
translates the result back into logical Model data. Contains no application
Behaviour, and never reaches into Database internals (engine, ORM,
connection, schema, migration, or commit/rollback mechanism) itself.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any, Literal

import my_database
from sqlalchemy.orm import Session

from my_backend._model_interface import BaseModel as ModelBaseModel

# Re-exported so Logic distinguishes outcomes without importing my_database directly.
NotFoundError = my_database.errors.NotFoundError
ConstraintViolationError = my_database.errors.ConstraintViolationError
StatusNotSupportedError = my_database.errors.StatusNotSupportedError
TransactionConflictError = my_database.errors.TransactionConflictError


def create[T: ModelBaseModel](record: T, *, session: Session | None = None) -> T:
    return my_database.add(record, session=session)


def get[T: ModelBaseModel](model_type: type[T], id: int, *, session: Session | None = None) -> T:
    return my_database.read(model_type, id, session=session)


def list_all[T: ModelBaseModel](
    model_type: type[T], *, limit: int = 50, offset: int = 0, session: Session | None = None
) -> Sequence[T]:
    return my_database.list_records(model_type, limit=limit, offset=offset, session=session)


def update[T: ModelBaseModel](
    model_type: type[T], id: int, patch: dict[str, Any], *, session: Session | None = None
) -> T:
    return my_database.edit(model_type, id, patch, session=session)


def remove(model_type: type[ModelBaseModel], id: int, *, session: Session | None = None) -> None:
    my_database.delete(model_type, id, session=session)


def set_status[T: ModelBaseModel](
    model_type: type[T], id: int, action: Literal["enable", "disable"], *, session: Session | None = None
) -> T:
    return my_database.set_status(model_type, id, action, session=session)


@contextmanager
def related_operations() -> Iterator[Session]:
    """One related-operation group carried through Database's own public
    transaction boundary: every operation in the group commits together or
    rolls back together.
    """

    with my_database.transaction() as session:
        yield session
