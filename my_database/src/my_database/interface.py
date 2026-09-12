"""The public, generic, Model-driven Database Interface.

Every operation accepts an imported Model type or instance and a resolved
Instance (explicit or default). No connection, ORM object, or mapping
detail crosses this boundary.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Literal

from my_model._base import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from my_database._base import get_runtime_config, get_session_factory, session_scope
from my_database._convert import row_to_model, to_row_kwargs
from my_database._mapping import EntityMapping, mapping_for


class NotFoundError(LookupError):
    def __init__(self, model_cls: type[BaseModel], record_id: int) -> None:
        super().__init__(f"No {model_cls.__name__} record with id={record_id!r}.")


class ConstraintViolationError(ValueError):
    """Raised when a write would violate a uniqueness or reference constraint."""


class UnsupportedOperationError(TypeError):
    """Raised when an operation does not apply to the given Model type."""


@dataclass
class Transaction:
    """A handle grouping related operations into one committed or rolled-back unit."""

    session: Session


@contextmanager
def transaction(instance: str | None = None) -> Generator[Transaction]:
    resolved = get_runtime_config().resolve(instance)
    factory = get_session_factory(resolved.key)
    session = factory()
    txn = Transaction(session=session)
    try:
        yield txn
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _run(instance: str | None, within: Transaction | None, body: Any) -> Any:
    if within is not None:
        result = body(within.session)
        within.session.flush()
        return result
    with session_scope(instance) as session:
        result = body(session)
        session.flush()
        return result


def add[T: BaseModel](
    record: T, *, instance: str | None = None, within: Transaction | None = None
) -> T:
    """Add/create: persist a new record from a Model instance."""
    mapping = mapping_for(type(record))
    row_kwargs = to_row_kwargs(mapping, record.model_dump())

    def body(session: Session) -> T:
        row = mapping.orm_cls(**row_kwargs)
        session.add(row)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise ConstraintViolationError(str(exc.orig)) from exc
        return row_to_model(mapping, row)

    return _run(instance, within, body)


def get[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> T | None:
    """Read by identifier. Returns None when no record exists with that id."""
    mapping = mapping_for(model_cls)

    def body(session: Session) -> T | None:
        row = session.get(mapping.orm_cls, record_id)
        return row_to_model(mapping, row) if row is not None else None

    return _run(instance, within, body)


def list_[T: BaseModel](
    model_cls: type[T],
    *,
    instance: str | None = None,
    within: Transaction | None = None,
    order_by: str | None = "id",
    limit: int | None = None,
    offset: int | None = None,
    **filters: Any,
) -> list[T]:
    """List with exact-match field criteria, deterministic ordering, and pagination."""
    mapping = mapping_for(model_cls)
    table = mapping.orm_cls.__table__

    def body(session: Session) -> list[T]:
        stmt = select(mapping.orm_cls)
        for field_name, value in filters.items():
            stmt = stmt.where(table.c[field_name] == value)
        if order_by is not None:
            stmt = stmt.order_by(table.c[order_by])
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        rows = session.execute(stmt).scalars().all()
        return [row_to_model(mapping, row) for row in rows]

    return _run(instance, within, body)


def update[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
    **changes: Any,
) -> T:
    """Edit/update: apply only the supplied fields, preserving omitted-vs-explicit-null semantics."""
    mapping = mapping_for(model_cls)
    row_changes = to_row_kwargs(mapping, changes) if changes else {}

    def body(session: Session) -> T:
        row = session.get(mapping.orm_cls, record_id)
        if row is None:
            raise NotFoundError(model_cls, record_id)
        for field_name, value in row_changes.items():
            setattr(row, field_name, value)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise ConstraintViolationError(str(exc.orig)) from exc
        return row_to_model(mapping, row)

    return _run(instance, within, body)


def delete[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> bool:
    """Delete by identifier. Returns True when a record was removed, False when none existed."""
    mapping = mapping_for(model_cls)

    def body(session: Session) -> bool:
        row = session.get(mapping.orm_cls, record_id)
        if row is None:
            return False
        session.delete(row)
        try:
            session.flush()
        except IntegrityError as exc:
            session.rollback()
            raise ConstraintViolationError(str(exc.orig)) from exc
        return True

    return _run(instance, within, body)


def set_status[T: BaseModel](
    model_cls: type[T],
    record_id: int,
    action: Literal["enable", "disable"],
    *,
    instance: str | None = None,
    within: Transaction | None = None,
) -> T:
    """Enable or disable a record. Only supported for a Model declaring a `status` field."""
    mapping = mapping_for(model_cls)
    if not has_status_field(mapping):
        raise UnsupportedOperationError(
            f"{model_cls.__name__} does not declare a status field."
        )
    return update(
        model_cls,
        record_id,
        instance=instance,
        within=within,
        status=(action == "enable"),
    )


def has_status_field(mapping: EntityMapping) -> bool:
    return "status" in mapping.orm_cls.__table__.columns
