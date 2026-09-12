"""The one generic, Model-driven data-access pipeline published through the
Database Interface: add, read, read-by-identifier, list, edit, delete, and
status, for any persistent Model.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from typing import Any, Literal

import my_model
from sqlalchemy import select
from sqlalchemy.orm import Session

from my_database._errors import NotFoundError, StatusNotSupportedError
from my_database._mapping import apply_write_transform, resolve_orm_type, row_to_model
from my_database._transactions import transaction


@contextmanager
def _resolve_session(
    instance: str | None, session: Session | None
) -> Iterator[tuple[Session, bool]]:
    if session is not None:
        yield session, False
        return
    with transaction(instance) as owned_session:
        yield owned_session, True


def add[T: my_model.BaseModel](
    record: T, *, instance: str | None = None, session: Session | None = None
) -> T:
    """Persist ``record`` as a new row. Any ``id`` on ``record`` is a
    placeholder for the required domain field; the persisted identity is
    always assigned by the storage structure.
    """

    model_type = type(record)
    orm_type = resolve_orm_type(model_type)
    values = record.model_dump(exclude={"id"})
    row = orm_type(**apply_write_transform(model_type, values))

    with _resolve_session(instance, session) as (active_session, _owned):
        active_session.add(row)
        active_session.flush()
        return row_to_model(model_type, row)


def read[T: my_model.BaseModel](
    model_type: type[T], id: int, *, instance: str | None = None, session: Session | None = None
) -> T:
    orm_type = resolve_orm_type(model_type)
    with _resolve_session(instance, session) as (active_session, _owned):
        row = active_session.get(orm_type, id)
        if row is None:
            raise NotFoundError(f"No {model_type.__name__} record with id={id!r}.")
        return row_to_model(model_type, row)


def list_records[T: my_model.BaseModel](
    model_type: type[T],
    *,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "id",
    instance: str | None = None,
    session: Session | None = None,
) -> Sequence[T]:
    orm_type = resolve_orm_type(model_type)
    column = getattr(orm_type, order_by)
    statement = select(orm_type).order_by(column).limit(limit).offset(offset)
    with _resolve_session(instance, session) as (active_session, _owned):
        rows = active_session.scalars(statement).all()
        return [row_to_model(model_type, row) for row in rows]


def edit[T: my_model.BaseModel](
    model_type: type[T],
    id: int,
    patch: dict[str, Any],
    *,
    instance: str | None = None,
    session: Session | None = None,
) -> T:
    """Apply a partial update: a key omitted from ``patch`` leaves the
    current value unchanged; a key present in ``patch`` (including an
    explicit ``None`` where the field permits it) replaces the current
    value. The full resulting record is re-validated against the Model
    before it is committed.
    """

    orm_type = resolve_orm_type(model_type)
    with _resolve_session(instance, session) as (active_session, _owned):
        row = active_session.get(orm_type, id)
        if row is None:
            raise NotFoundError(f"No {model_type.__name__} record with id={id!r}.")

        current = row_to_model(model_type, row).model_dump()
        merged = {**current, **patch}
        validated = model_type(**merged)  # raises pydantic.ValidationError if invalid

        transformed_patch = apply_write_transform(model_type, patch)
        for field_name, value in transformed_patch.items():
            if field_name == "id":
                continue
            setattr(row, field_name, value)
        active_session.flush()
        return validated.model_copy(update={"id": row.id})  # pyright: ignore[reportAttributeAccessIssue]


def delete(
    model_type: type[my_model.BaseModel],
    id: int,
    *,
    instance: str | None = None,
    session: Session | None = None,
) -> None:
    orm_type = resolve_orm_type(model_type)
    with _resolve_session(instance, session) as (active_session, _owned):
        row = active_session.get(orm_type, id)
        if row is None:
            raise NotFoundError(f"No {model_type.__name__} record with id={id!r}.")
        active_session.delete(row)
        active_session.flush()


def set_status[T: my_model.BaseModel](
    model_type: type[T],
    id: int,
    action: Literal["enable", "disable"],
    *,
    instance: str | None = None,
    session: Session | None = None,
) -> T:
    if "status" not in model_type.model_fields:
        raise StatusNotSupportedError(f"{model_type.__name__} does not declare a status field.")
    return edit(
        model_type, id, {"status": action == "enable"}, instance=instance, session=session
    )
