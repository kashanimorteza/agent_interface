"""The generic Model-driven operation pipeline.

Every function takes an open SQLAlchemy ``Session`` as its first argument and a
Model key as its second. Functions flush but never commit; the caller (the
Database Interface facade) owns the transaction. Returned records are plain
dicts that never contain credential columns.
"""

from __future__ import annotations

from typing import Any, Mapping

from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from ta_database.data_logic.errors import (
    IntegrityViolation,
    InvalidAction,
    InvalidField,
    RecordNotFound,
    UnsupportedOperation,
)
from ta_database.data_logic.resolution import primary_key_name, resolve_model, validate_fields
from ta_database.data_logic.serialization import to_record
from ta_database.storage_adapter.credentials.transform import apply_write_transforms

STATUS_FIELD = "status"
STATUS_ACTIONS = {"enable": True, "disable": False}


def _flush_or_integrity(session, action: str) -> None:
    try:
        session.flush()
    except IntegrityError as exc:
        session.rollback()
        raise IntegrityViolation(f"{action} rejected by a storage rule: {exc.orig}") from exc


def _get_or_404(session, mapped_class: type, record_id: Any):
    instance = session.get(mapped_class, record_id)
    if instance is None:
        raise RecordNotFound(f"{mapped_class.__tablename__} has no record with {primary_key_name(mapped_class)}={record_id!r}")
    return instance


def create(session, model_key: str, data: Mapping[str, Any]) -> dict[str, Any]:
    """Insert one record for the Model from a mapping of field values."""
    mapped_class = resolve_model(model_key)
    validate_fields(mapped_class, data)
    instance = mapped_class(**apply_write_transforms(mapped_class, data))
    session.add(instance)
    _flush_or_integrity(session, "create")
    return to_record(instance)


def read(session, model_key: str, record_id: Any) -> dict[str, Any] | None:
    """Return one record by primary key, or None when absent."""
    mapped_class = resolve_model(model_key)
    instance = session.get(mapped_class, record_id)
    return None if instance is None else to_record(instance)


def list_records(session, model_key: str, filters: Mapping[str, Any] | None = None, order_by: str | None = None,
                 limit: int | None = None, offset: int | None = None) -> list[dict[str, Any]]:
    """Return records of the Model with equality filters, ordering, and paging."""
    mapped_class = resolve_model(model_key)
    table = mapped_class.__table__
    stmt = select(mapped_class)
    if filters:
        validate_fields(mapped_class, filters, allow_primary_key=True)
        for key, value in filters.items():
            stmt = stmt.where(table.c[key] == value)
    if order_by:
        descending = order_by.startswith("-")
        column_name = order_by[1:] if descending else order_by
        validate_fields(mapped_class, [column_name], allow_primary_key=True)
        column = table.c[column_name]
        stmt = stmt.order_by(column.desc() if descending else column.asc())
    else:
        stmt = stmt.order_by(table.c[primary_key_name(mapped_class)].asc())
    if offset:
        stmt = stmt.offset(offset)
    if limit is not None:
        stmt = stmt.limit(limit)
    return [to_record(instance) for instance in session.scalars(stmt)]


def update(session, model_key: str, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
    """Apply field values to one record by primary key and return it."""
    mapped_class = resolve_model(model_key)
    validate_fields(mapped_class, data)
    instance = _get_or_404(session, mapped_class, record_id)
    for key, value in apply_write_transforms(mapped_class, data).items():
        setattr(instance, key, value)
    _flush_or_integrity(session, "update")
    return to_record(instance)


def delete(session, model_key: str, record_id: Any) -> None:
    """Remove one record by primary key; RESTRICT rules may refuse it."""
    mapped_class = resolve_model(model_key)
    instance = _get_or_404(session, mapped_class, record_id)
    session.delete(instance)
    _flush_or_integrity(session, "delete")


def status(session, model_key: str, record_id: Any, action: str) -> dict[str, Any]:
    """Enable or disable one record of a Model that declares a status field."""
    if action not in STATUS_ACTIONS:
        raise InvalidAction(f"status action must be one of {', '.join(STATUS_ACTIONS)}; got {action!r}")
    mapped_class = resolve_model(model_key)
    if STATUS_FIELD not in mapped_class.__table__.columns:
        raise UnsupportedOperation(f"{mapped_class.__tablename__} has no {STATUS_FIELD} field")
    instance = _get_or_404(session, mapped_class, record_id)
    setattr(instance, STATUS_FIELD, STATUS_ACTIONS[action])
    _flush_or_integrity(session, "status")
    return to_record(instance)


def execute_sql(session, command: str, params: Mapping[str, Any] | None = None) -> list[dict[str, Any]] | int:
    """Run one parameterized SQL command; return row dicts or the affected rowcount."""
    if not isinstance(command, str) or not command.strip():
        raise InvalidField("command must be a non-empty SQL string")
    result = session.execute(text(command), dict(params or {}))
    if result.returns_rows:
        return [dict(row._mapping) for row in result]
    return result.rowcount
