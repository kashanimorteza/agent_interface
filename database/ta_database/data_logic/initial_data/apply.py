"""Idempotent application and removal of the project's initial records."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select

from ta_database.data_logic.initial_data.records import GENERATE, SEED
from ta_database.data_logic.resolution import resolve_model
from ta_database.storage_adapter.credentials.generation import generate_secret
from ta_database.storage_adapter.credentials.transform import apply_write_transforms


def _find(session, mapped_class: type, natural_key: tuple[str, ...], record: dict[str, Any]):
    table = mapped_class.__table__
    stmt = select(mapped_class)
    for key in natural_key:
        stmt = stmt.where(table.c[key] == record[key])
    return session.scalars(stmt).first()


def apply_seed(session) -> dict[str, Any]:
    """Insert every declared initial record that is not yet present, in dependency order.

    Returns ``{"inserted": {model_key: count}, "generated": {(model_key, natural_key_values, field): plain_value}}``.
    Generated plain values are returned once so the operator can record them; they are never persisted.
    """
    inserted: dict[str, int] = {}
    generated: dict[tuple[str, tuple[Any, ...], str], str] = {}
    for model_key, natural_key, records in SEED:
        mapped_class = resolve_model(model_key)
        inserted[model_key] = 0
        for record in records:
            if _find(session, mapped_class, natural_key, record) is not None:
                continue
            values = dict(record)
            key_values = tuple(record[k] for k in natural_key)
            for field, value in list(values.items()):
                if value is GENERATE:
                    plain = generate_secret()
                    values[field] = plain
                    generated[(model_key, key_values, field)] = plain
            session.add(mapped_class(**apply_write_transforms(mapped_class, values)))
            inserted[model_key] += 1
        session.flush()
    return {"inserted": inserted, "generated": generated}


def remove_seed(session) -> dict[str, int]:
    """Delete the declared initial records by natural key, in reverse dependency order."""
    removed: dict[str, int] = {}
    for model_key, natural_key, records in reversed(SEED):
        mapped_class = resolve_model(model_key)
        removed[model_key] = 0
        for record in records:
            instance = _find(session, mapped_class, natural_key, record)
            if instance is not None:
                session.delete(instance)
                removed[model_key] += 1
        session.flush()
    return removed
