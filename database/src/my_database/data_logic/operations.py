"""Generic Model-driven operation pipeline — one implementation for every persistent Model.

Every function takes a Session and a Model key; the caller owns the transaction. Records are returned
as plain dicts without credential columns; every rejection is a Database error type.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from my_database.data_logic.registry import ModelInfo, get_model
from my_database.errors import (
    ConstraintViolationError,
    InvalidActionError,
    RecordNotFoundError,
    UnknownFieldError,
    UnsupportedOperationError,
)
from my_database.storage_adapter.credentials import transform_for_storage

STATUS_ACTIONS: Mapping[str, bool] = {"enable": True, "disable": False}


def to_record(info: ModelInfo, instance: Any) -> dict[str, Any]:
    """The instance as a mapping of column name to value, excluding credential columns."""
    return {c: getattr(instance, c) for c in info.columns if c not in info.credential_fields}


def _validate_write(info: ModelInfo, data: Mapping[str, Any]) -> None:
    unknown = [f for f in data if f not in info.columns]
    if unknown:
        raise UnknownFieldError(f"{info.key} has no field {', '.join(map(repr, unknown))}")
    if info.primary_key in data:
        raise UnknownFieldError(f"the primary key {info.primary_key!r} of {info.key} is generated and may not be supplied")


def _check_queryable(info: ModelInfo, field: str) -> None:
    if field not in info.columns:
        raise UnknownFieldError(f"{info.key} has no field {field!r}")
    if field in info.credential_fields:
        raise UnknownFieldError(f"credential field {field!r} of {info.key} cannot be used for filtering or ordering")


def _prepare(info: ModelInfo, data: Mapping[str, Any]) -> dict[str, Any]:
    return {
        f: transform_for_storage(v, info.credential_fields[f]) if f in info.credential_fields else v
        for f, v in data.items()
    }


def _flush(session: Session) -> None:
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise ConstraintViolationError(str(exc.orig)) from None


def _get_or_raise(session: Session, info: ModelInfo, record_id: Any) -> Any:
    instance = session.get(info.mapped_class, record_id)
    if instance is None:
        raise RecordNotFoundError(f"{info.key} {record_id!r} does not exist")
    return instance


def create(session: Session, model: str, data: Mapping[str, Any]) -> dict[str, Any]:
    """Insert one record and return it."""
    info = get_model(model)
    _validate_write(info, data)
    instance = info.mapped_class(**_prepare(info, data))
    session.add(instance)
    _flush(session)
    return to_record(info, instance)


def read(session: Session, model: str, record_id: Any) -> dict[str, Any] | None:
    """One record by primary key, or None when absent."""
    info = get_model(model)
    instance = session.get(info.mapped_class, record_id)
    return None if instance is None else to_record(info, instance)


def list_records(
    session: Session,
    model: str,
    *,
    filters: Mapping[str, Any] | None = None,
    order_by: Sequence[str] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[dict[str, Any]]:
    """Records matching equality filters, ordered (leading '-' = descending; default primary key) and paged."""
    info = get_model(model)
    cls = info.mapped_class
    statement = select(cls)
    for field, value in (filters or {}).items():
        _check_queryable(info, field)
        statement = statement.where(getattr(cls, field) == value)
    for spec in order_by or [info.primary_key]:
        descending = spec.startswith("-")
        field = spec[1:] if descending else spec
        _check_queryable(info, field)
        column = getattr(cls, field)
        statement = statement.order_by(column.desc() if descending else column.asc())
    if limit is not None:
        statement = statement.limit(limit)
    if offset:
        statement = statement.offset(offset)
    return [to_record(info, instance) for instance in session.scalars(statement)]


def update(session: Session, model: str, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
    """Apply a partial update to one record and return it."""
    info = get_model(model)
    _validate_write(info, data)
    instance = _get_or_raise(session, info, record_id)
    for field, value in _prepare(info, data).items():
        setattr(instance, field, value)
    _flush(session)
    return to_record(info, instance)


def delete(session: Session, model: str, record_id: Any) -> None:
    """Remove one record; a RESTRICT referential action raises ConstraintViolationError."""
    info = get_model(model)
    instance = _get_or_raise(session, info, record_id)
    session.delete(instance)
    _flush(session)


def set_status(session: Session, model: str, record_id: Any, action: str) -> dict[str, Any]:
    """Enable or disable one record through its status field."""
    info = get_model(model)
    if not info.has_status:
        raise UnsupportedOperationError(f"{info.key} has no status field; the status operation is not available")
    if action not in STATUS_ACTIONS:
        raise InvalidActionError(f"status action must be one of {', '.join(STATUS_ACTIONS)}; got {action!r}")
    instance = _get_or_raise(session, info, record_id)
    instance.status = STATUS_ACTIONS[action]
    _flush(session)
    return to_record(info, instance)
