"""The one generic, Model-driven data-access pipeline.

Every operation is parameterized only by an imported ``my_model`` type (never
a Model name string) and plain criteria or field values. The same pipeline
serves every persistent Model; there is no per-Model implementation here.
"""

from __future__ import annotations

import builtins
from typing import Literal

import my_model as m
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import _credentials, _session
from ._orm import MODEL_TO_ROW, Base
from .exceptions import ConstraintViolation, NotFound, UnsupportedOperation, ValidationFailed
from .transactions import Unit

_REDACTED = "••••••••"


def _row_class(model_type: type[m.BaseModel]) -> type[Base]:
    try:
        return MODEL_TO_ROW[model_type]
    except KeyError:
        raise ValueError(f"{model_type!r} is not a persistent Model known to my_database") from None


def _session_for(
    unit: Unit | None, *, standalone_instance: str | None = None
) -> tuple[Session, bool]:
    if unit is not None:
        return unit.session, False
    return _session.session_for(standalone_instance), True


def _row_to_dict(row: Base) -> dict:
    mapper = row.__mapper__
    return {column.key: getattr(row, column.key) for column in mapper.columns}


def _redact(model_type: type[m.BaseModel], data: dict) -> dict:
    redacted = dict(data)
    for field in model_type.credential_fields:
        if field in redacted and redacted[field] is not None:
            redacted[field] = _REDACTED
    return redacted


def _to_model(model_type: type[m.BaseModel], row: Base) -> m.BaseModel:
    data = _redact(model_type, _row_to_dict(row))
    return model_type(**data)


def _validate(model_type: type[m.BaseModel], data: dict) -> m.BaseModel:
    try:
        return model_type(**data)
    except ValidationError as error:
        raise ValidationFailed(str(error)) from error


def add(
    model_type: type[m.BaseModel],
    *,
    unit: Unit | None = None,
    instance: str | None = None,
    **fields,
) -> m.BaseModel:
    """Add (create) one record from plain field values, applying Model validation."""
    row_cls = _row_class(model_type)
    validated = _validate(model_type, fields)
    payload = validated.model_dump(exclude={"id"})
    for field in model_type.credential_fields:
        if payload.get(field) is not None:
            payload[field] = _credentials.transform_for_storage(field, payload[field])

    session, standalone = _session_for(unit, standalone_instance=instance)
    row = row_cls(**payload)
    session.add(row)
    try:
        session.flush()
        if standalone:
            session.commit()
    except IntegrityError as error:
        session.rollback()
        raise ConstraintViolation(str(error)) from error
    finally:
        if standalone:
            session.close()

    generated_id = getattr(row, "id")  # noqa: B009 - Base has no `id`; every concrete row class does
    return validated.model_copy(
        update={"id": generated_id, **{f: _REDACTED for f in model_type.credential_fields}}
    )


def get(
    model_type: type[m.BaseModel],
    id: int,
    *,
    unit: Unit | None = None,
    instance: str | None = None,
) -> m.BaseModel:
    """Read one record by its typed identifier. Raises :class:`NotFound` when absent."""
    row_cls = _row_class(model_type)
    session, standalone = _session_for(unit, standalone_instance=instance)
    try:
        row = session.get(row_cls, id)
        if row is None:
            raise NotFound(f"{model_type.__name__} {id} does not exist")
        return _to_model(model_type, row)
    finally:
        if standalone:
            session.close()


def list(  # noqa: A001 - "list" is the Database Standard's own operation name
    model_type: type[m.BaseModel],
    *,
    unit: Unit | None = None,
    instance: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    **criteria,
) -> builtins.list[m.BaseModel]:
    """List records matching exact-value criteria, ordered deterministically by id."""
    row_cls = _row_class(model_type)
    session, standalone = _session_for(unit, standalone_instance=instance)
    try:
        stmt = select(row_cls).order_by(getattr(row_cls, "id"))  # noqa: B009 - see add()
        for field, value in criteria.items():
            stmt = stmt.where(getattr(row_cls, field) == value)
        if offset:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        rows = session.execute(stmt).scalars().all()
        return [_to_model(model_type, row) for row in rows]
    finally:
        if standalone:
            session.close()


def update(
    model_type: type[m.BaseModel],
    id: int,
    *,
    unit: Unit | None = None,
    instance: str | None = None,
    **fields,
) -> m.BaseModel:
    """Edit (partially update) one record. An omitted field is left unchanged."""
    row_cls = _row_class(model_type)
    session, standalone = _session_for(unit, standalone_instance=instance)
    try:
        row = session.get(row_cls, id)
        if row is None:
            raise NotFound(f"{model_type.__name__} {id} does not exist")

        merged = _row_to_dict(row) | fields
        _validate(model_type, merged)  # raises ValidationFailed on a violated Model rule

        for field, value in fields.items():
            if field in model_type.credential_fields and value is not None:
                value = _credentials.transform_for_storage(field, value)
            setattr(row, field, value)

        try:
            session.flush()
            if standalone:
                session.commit()
        except IntegrityError as error:
            session.rollback()
            raise ConstraintViolation(str(error)) from error

        return _to_model(model_type, row)
    finally:
        if standalone:
            session.close()


def delete(
    model_type: type[m.BaseModel],
    id: int,
    *,
    unit: Unit | None = None,
    instance: str | None = None,
) -> None:
    """Delete one record. Raises :class:`NotFound` when absent, or :class:`ConstraintViolation`
    when another record still references it.
    """
    row_cls = _row_class(model_type)
    session, standalone = _session_for(unit, standalone_instance=instance)
    try:
        row = session.get(row_cls, id)
        if row is None:
            raise NotFound(f"{model_type.__name__} {id} does not exist")
        session.delete(row)
        try:
            session.flush()
            if standalone:
                session.commit()
        except IntegrityError as error:
            session.rollback()
            raise ConstraintViolation(str(error)) from error
    finally:
        if standalone:
            session.close()


def set_status(
    model_type: type[m.BaseModel],
    id: int,
    action: Literal["enable", "disable"],
    *,
    unit: Unit | None = None,
    instance: str | None = None,
) -> m.BaseModel:
    """Enable or disable a record. Available only for a Model declaring a ``status`` field."""
    if "status" not in model_type.model_fields:
        raise UnsupportedOperation(f"{model_type.__name__} does not declare a status field")
    if action not in ("enable", "disable"):
        raise ValueError("action must be 'enable' or 'disable'")
    return update(model_type, id, unit=unit, instance=instance, status=(action == "enable"))
