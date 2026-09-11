"""Data Logic: one generic, Model-driven operation pipeline for every persistent Model."""

from __future__ import annotations

import re
from contextlib import contextmanager

from pydantic import ValidationError
from sqlalchemy import Connection, delete, insert, select, update as sa_update
from sqlalchemy.exc import IntegrityError

from . import _credentials, _engine, _schema

_DDL_KEYWORDS = re.compile(r"\b(CREATE|ALTER|DROP|TRUNCATE|ATTACH|DETACH|PRAGMA)\b", re.IGNORECASE)


class RejectedOperationError(ValueError):
    """A requested operation could not be performed under Database's protections."""


class UnsupportedOperationError(ValueError):
    pass


def _table(model_cls):
    return _schema.build_all_tables()[model_cls]


def _redact(model_cls, row: dict) -> dict:
    credential_fields = set(model_cls.credential_fields())
    return {k: v for k, v in row.items() if k not in credential_fields}


def _apply_credential_transforms(model_cls, values: dict) -> dict:
    transformed = dict(values)
    for field in model_cls.credential_fields():
        if field in transformed and transformed[field] is not None:
            transformed[field] = _credentials.transform(model_cls, field, transformed[field])
    return transformed


@contextmanager
def transaction(instance: str | None = None):
    """Groups related operations on one Instance so they commit or roll back together."""
    engine = _engine.engine_for(instance)
    with engine.begin() as conn:
        yield conn


@contextmanager
def _connection(instance: str | None, conn: Connection | None):
    if conn is not None:
        yield conn
        return
    engine = _engine.engine_for(instance)
    with engine.begin() as new_conn:
        yield new_conn


def create(model_cls, *, instance: str | None = None, conn: Connection | None = None, **values) -> dict:
    validated = model_cls(**values)  # Model validation of the supplied data.
    payload = validated.model_dump(exclude={"id"})
    payload = _apply_credential_transforms(model_cls, payload)
    table = _table(model_cls)
    with _connection(instance, conn) as c:
        try:
            result = c.execute(insert(table).values(**payload))
        except IntegrityError as e:
            raise RejectedOperationError(str(e.orig)) from e
        row = c.execute(select(table).where(table.c.id == result.inserted_primary_key[0])).mappings().one()
    return _redact(model_cls, dict(row))


def get(model_cls, id_: int, *, instance: str | None = None, conn: Connection | None = None) -> dict | None:
    table = _table(model_cls)
    with _connection(instance, conn) as c:
        row = c.execute(select(table).where(table.c.id == id_)).mappings().one_or_none()
    return _redact(model_cls, dict(row)) if row is not None else None


def list_(model_cls, *, instance: str | None = None, conn: Connection | None = None, **filters) -> list[dict]:
    table = _table(model_cls)
    stmt = select(table)
    for key, value in filters.items():
        stmt = stmt.where(table.c[key] == value)
    with _connection(instance, conn) as c:
        rows = c.execute(stmt).mappings().all()
    return [_redact(model_cls, dict(r)) for r in rows]


def update(model_cls, id_: int, *, instance: str | None = None, conn: Connection | None = None, **values) -> dict:
    table = _table(model_cls)
    with _connection(instance, conn) as c:
        existing = c.execute(select(table).where(table.c.id == id_)).mappings().one_or_none()
        if existing is None:
            raise RejectedOperationError(f"No {model_cls.__name__} with id={id_} exists.")

        # Re-validate the complete resulting record. Credential fields not
        # being changed reuse their stored (already-transformed) string
        # purely to satisfy the Model's type constraint; only fields present
        # in this call's own `values` are re-transformed and written.
        merged = {**dict(existing), **values}
        merged.pop("id", None)
        model_cls(**merged)  # raises ValidationError on a rule violation

        payload = _apply_credential_transforms(model_cls, values)
        if payload:
            try:
                c.execute(sa_update(table).where(table.c.id == id_).values(**payload))
            except IntegrityError as e:
                raise RejectedOperationError(str(e.orig)) from e
        row = c.execute(select(table).where(table.c.id == id_)).mappings().one()
    return _redact(model_cls, dict(row))


def delete_(model_cls, id_: int, *, instance: str | None = None, conn: Connection | None = None) -> bool:
    table = _table(model_cls)
    with _connection(instance, conn) as c:
        result = c.execute(delete(table).where(table.c.id == id_))
    return result.rowcount > 0


def status(model_cls, id_: int, action: str, *, instance: str | None = None, conn: Connection | None = None) -> dict:
    if action not in ("enable", "disable"):
        raise UnsupportedOperationError(f"Unsupported status action {action!r}; expected 'enable' or 'disable'.")
    if "status" not in model_cls.model_fields:
        raise UnsupportedOperationError(f"{model_cls.__name__} declares no status field.")
    return update(model_cls, id_, instance=instance, conn=conn, status=(action == "enable"))


_MODEL_BY_TABLE = None


def _model_for_table(name: str):
    global _MODEL_BY_TABLE
    if _MODEL_BY_TABLE is None:
        tables = _schema.build_all_tables()
        _MODEL_BY_TABLE = {t.name: mc for mc, t in tables.items()}
    return _MODEL_BY_TABLE.get(name)


def execute_sql(sql: str, params: dict | None = None, *, instance: str | None = None, conn: Connection | None = None):
    """Controlled, parameterized SQL for operations standard Model operations cannot express.

    Rejects structural changes outright and, for a statement whose affected
    table and resulting row can be identified, re-validates that row against
    its Model before committing and redacts credential columns from any
    returned rows.
    """
    from sqlalchemy import text

    if _DDL_KEYWORDS.search(sql):
        raise RejectedOperationError("Structural changes are rejected on the controlled SQL route; use Migration.")

    tables = _schema.build_all_tables()
    known_names = {t.name for t in tables.values()}
    mentioned = [name for name in known_names if re.search(rf"\b{name}\b", sql, re.IGNORECASE)]
    if len(mentioned) != 1:
        raise RejectedOperationError(
            "Cannot establish which single mapped table this command affects; the controlled SQL route "
            "accepts only statements naming exactly one mapped table."
        )
    model_cls = _model_for_table(mentioned[0])
    kind = sql.strip().split(None, 1)[0].upper()

    if kind in ("INSERT", "UPDATE") and "RETURNING" not in sql.upper():
        raise RejectedOperationError(
            "A command that writes data must use RETURNING so its resulting row can be validated before commit."
        )

    with _connection(instance, conn) as c:
        result = c.execute(text(sql), params or {})

        if kind in ("INSERT", "UPDATE"):
            written_rows = result.mappings().all()
            for row in written_rows:
                record = dict(row)
                record.pop("id", None)
                try:
                    model_cls(**record)  # Re-validates the resulting data against the Model.
                except ValidationError as e:
                    raise RejectedOperationError(f"Resulting data violates the Model: {e}") from e
            return [_redact(model_cls, dict(r)) for r in written_rows]

        if result.returns_rows:
            return [_redact(model_cls, dict(r)) for r in result.mappings().all()]
    return None
