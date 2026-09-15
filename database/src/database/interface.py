"""The generic, Model-driven Database Interface.

One shared pipeline serves every persistent Domain Definition: create,
get_by_id, list_, search, update, delete, enable/disable, an explicit
Transaction boundary, and a capability-restricted controlled-command route.
No operation ever exposes a credential field's stored or original value.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

from model.foundation import DomainModel
from sqlalchemy import Connection, delete, insert, select, text, update as sa_update
from sqlalchemy.engine import Engine

from database.bootstrap import ensure_ready
from database.credentials import REDACTED, apply_at_rest_treatment
from database.exceptions import ActivationNotSupportedError, ControlledCommandRejectedError
from database.mapping import MAPPED_TABLES, contract_for, table_for

M = TypeVar("M", bound=DomainModel)

_command_logger = logging.getLogger("database.controlled_command")

_FORBIDDEN_KEYWORDS = re.compile(
    r"\b(CREATE|ALTER|DROP|GRANT|REVOKE|PRAGMA|ATTACH|DETACH|VACUUM)\b", re.IGNORECASE
)
_ALLOWED_LEADING_VERBS = ("SELECT", "INSERT", "UPDATE", "DELETE")

# Every column name, across every mapped Domain Definition, that Model classifies
# as a credential — redacted from execute_command results regardless of which
# table(s) a query touches, since the route accepts arbitrary parameterized SQL
# rather than a typed Model that would let per-model redaction apply directly.
_ALL_CREDENTIAL_COLUMN_NAMES: set[str] = {
    field.name
    for mapped in MAPPED_TABLES.values()
    for field in mapped.contract.fields
    if field.meta.credential is not None
}


def _engine(instance: str | None) -> Engine:
    return ensure_ready(instance)


def _credential_fields(model: type[M]) -> set[str]:
    contract = contract_for(model)
    return {f.name for f in contract.fields if f.meta.credential is not None}


def _apply_credential_treatment(model: type[M], values: dict[str, Any]) -> dict[str, Any]:
    contract = contract_for(model)
    by_name = {f.name: f.meta for f in contract.fields}
    result = dict(values)
    for name, value in values.items():
        meta = by_name.get(name)
        if meta is not None and meta.credential is not None and value is not None:
            result[name] = apply_at_rest_treatment(meta.credential, value)
    return result


def _redact(model: type[M], row: dict[str, Any]) -> dict[str, Any]:
    credential_fields = _credential_fields(model)
    return {k: (REDACTED if k in credential_fields else v) for k, v in row.items()}


def _row_to_model(model: type[M], row: dict[str, Any]) -> M:
    return model.model_validate(_redact(model, row))


class Transaction:
    """Groups related Database Interface calls on one Instance into one atomic unit."""

    def __init__(self, connection: Connection) -> None:
        self.connection = connection


@contextmanager
def transaction(instance: str | None = None) -> Iterator[Transaction]:
    engine = _engine(instance)
    with engine.begin() as connection:
        yield Transaction(connection)


def _connection(instance: str | None, tx: Transaction | None) -> tuple[Connection, bool]:
    """Return (connection, owns_transaction). A standalone call owns and commits its own unit."""
    if tx is not None:
        return tx.connection, False
    engine = _engine(instance)
    conn = engine.connect()
    return conn, True


def create(model: type[M], *, instance: str | None = None, tx: Transaction | None = None, **fields: Any) -> M:
    table = table_for(model)
    values = _apply_credential_treatment(model, fields)
    conn, owns = _connection(instance, tx)
    try:
        result = conn.execute(insert(table).values(**values))
        if owns:
            conn.commit()
        new_id = result.inserted_primary_key[0]
        row = conn.execute(select(table).where(table.c.id == new_id)).mappings().one()
        return _row_to_model(model, dict(row))
    finally:
        if owns:
            conn.close()


def get_by_id(model: type[M], id_: int, *, instance: str | None = None, tx: Transaction | None = None) -> M | None:
    table = table_for(model)
    conn, owns = _connection(instance, tx)
    try:
        row = conn.execute(select(table).where(table.c.id == id_)).mappings().first()
        return _row_to_model(model, dict(row)) if row is not None else None
    finally:
        if owns:
            conn.close()


def list_(
    model: type[M],
    *,
    limit: int | None = None,
    offset: int | None = None,
    instance: str | None = None,
    tx: Transaction | None = None,
) -> list[M]:
    table = table_for(model)
    conn, owns = _connection(instance, tx)
    try:
        stmt = select(table)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        rows = conn.execute(stmt).mappings().all()
        return [_row_to_model(model, dict(r)) for r in rows]
    finally:
        if owns:
            conn.close()


def search(model: type[M], *, instance: str | None = None, tx: Transaction | None = None, **criteria: Any) -> list[M]:
    table = table_for(model)
    conn, owns = _connection(instance, tx)
    try:
        stmt = select(table)
        for key, value in criteria.items():
            stmt = stmt.where(table.c[key] == value)
        rows = conn.execute(stmt).mappings().all()
        return [_row_to_model(model, dict(r)) for r in rows]
    finally:
        if owns:
            conn.close()


def update(
    model: type[M], id_: int, *, instance: str | None = None, tx: Transaction | None = None, **fields: Any
) -> M:
    table = table_for(model)
    values = _apply_credential_treatment(model, fields)
    conn, owns = _connection(instance, tx)
    try:
        conn.execute(sa_update(table).where(table.c.id == id_).values(**values))
        if owns:
            conn.commit()
        row = conn.execute(select(table).where(table.c.id == id_)).mappings().one()
        return _row_to_model(model, dict(row))
    finally:
        if owns:
            conn.close()


def delete(model: type[M], id_: int, *, instance: str | None = None, tx: Transaction | None = None) -> None:
    table = table_for(model)
    conn, owns = _connection(instance, tx)
    try:
        conn.execute(delete(table).where(table.c.id == id_))
        if owns:
            conn.commit()
    finally:
        if owns:
            conn.close()


def _set_active(
    model: type[M], id_: int, value: bool, *, instance: str | None, tx: Transaction | None
) -> M:
    contract = contract_for(model)
    if not any(f.name == "is_active" for f in contract.fields):
        raise ActivationNotSupportedError(
            f"{model.__name__} declares no active-state field; activation is not supported."
        )
    return update(model, id_, instance=instance, tx=tx, is_active=value)


def enable(model: type[M], id_: int, *, instance: str | None = None, tx: Transaction | None = None) -> M:
    return _set_active(model, id_, True, instance=instance, tx=tx)


def disable(model: type[M], id_: int, *, instance: str | None = None, tx: Transaction | None = None) -> M:
    return _set_active(model, id_, False, instance=instance, tx=tx)


def execute_command(
    sql: str,
    params: dict[str, Any] | None = None,
    *,
    instance: str | None = None,
    tx: Transaction | None = None,
) -> list[dict[str, Any]]:
    """Capability-restricted, parameterized route for data operations the standard
    pipeline cannot express. Rejects any structural change, privilege change, or
    Migration operation. Never accepts string-formatted values — bind parameters only.
    """
    stripped = sql.strip()
    leading_verb = stripped.split(None, 1)[0].upper() if stripped else ""
    if leading_verb not in _ALLOWED_LEADING_VERBS or _FORBIDDEN_KEYWORDS.search(stripped):
        raise ControlledCommandRejectedError(
            "Only parameterized SELECT/INSERT/UPDATE/DELETE data operations are permitted; "
            "structural, privilege, and Migration commands are rejected."
        )

    conn, owns = _connection(instance, tx)
    try:
        result = conn.execute(text(sql), params or {})
        _command_logger.info("controlled_command executed: %s", leading_verb)
        rows: list[dict[str, Any]] = []
        if result.returns_rows:
            rows = [
                {
                    k: (REDACTED if k in _ALL_CREDENTIAL_COLUMN_NAMES else v)
                    for k, v in dict(r).items()
                }
                for r in result.mappings().all()
            ]
        if owns:
            conn.commit()
        return rows
    finally:
        if owns:
            conn.close()
