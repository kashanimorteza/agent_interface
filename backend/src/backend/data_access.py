"""Data Access: the only Backend module that imports the Database package.

Translates Logic's data requests into calls on the generic Database
interface and back. Contains no application Behaviour of its own.

Each function is generic in the Model type so a caller passing, for example,
``my_model.Broker`` gets back a ``Broker`` statically, not just the shared
``BaseModel`` base. My_database's own operations return the base type; the
``cast`` calls below restate, once in this single translation point, the
narrowing that is always true at runtime because the same ``model_type`` was
just passed in.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Literal, cast

import my_database as _db
import my_model as m

# Re-exported so Logic never needs its own import of my_database.exceptions.
from my_database.exceptions import (  # noqa: F401
    ConstraintViolation,
    DatabaseError,
    NotFound,
    UnsupportedOperation,
    ValidationFailed,
)
from my_database.transactions import Unit


def create[ModelT: m.BaseModel](
    model_type: type[ModelT], *, unit: Unit | None = None, **fields
) -> ModelT:
    return cast(ModelT, _db.operations.add(model_type, unit=unit, **fields))


def get[ModelT: m.BaseModel](
    model_type: type[ModelT], id: int, *, unit: Unit | None = None
) -> ModelT:
    return cast(ModelT, _db.operations.get(model_type, id, unit=unit))


def list_records[ModelT: m.BaseModel](
    model_type: type[ModelT],
    *,
    unit: Unit | None = None,
    limit: int | None = None,
    offset: int = 0,
    **criteria,
) -> list[ModelT]:
    records = _db.operations.list(model_type, unit=unit, limit=limit, offset=offset, **criteria)
    return cast(list[ModelT], records)


def update[ModelT: m.BaseModel](
    model_type: type[ModelT], id: int, *, unit: Unit | None = None, **fields
) -> ModelT:
    return cast(ModelT, _db.operations.update(model_type, id, unit=unit, **fields))


def delete(model_type: type[m.BaseModel], id: int, *, unit: Unit | None = None) -> None:
    _db.operations.delete(model_type, id, unit=unit)


def set_status[ModelT: m.BaseModel](
    model_type: type[ModelT],
    id: int,
    action: Literal["enable", "disable"],
    *,
    unit: Unit | None = None,
) -> ModelT:
    return cast(ModelT, _db.operations.set_status(model_type, id, action, unit=unit))


@contextmanager
def transaction() -> Iterator[Unit]:
    """Group related Data Access calls into one Database transaction.

    Pass the yielded unit as ``unit=`` to every call that must commit or
    roll back together; Database owns commit, rollback, and cleanup.
    """
    with _db.transactions.unit() as unit:
        yield unit
