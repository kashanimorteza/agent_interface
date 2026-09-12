"""Conversion between a Model instance and its persistence row.

Applies each credential field's resolved at-rest transformation on the way
in, and the corresponding read-time projection on the way out: a decrypted
value for a recoverable ("encrypted") credential, and a fixed redaction
marker for an irreversible ("hash") credential — the storage representation
itself is never returned to a consumer.
"""

from __future__ import annotations

from typing import Any

from my_database._config import resolve_encryption_key
from my_database._credentials import decrypt_value, encrypt_value, hash_value
from my_database._mapping import EntityMapping

REDACTED = "<redacted>"


def to_row_kwargs(mapping: EntityMapping, data: dict[str, Any]) -> dict[str, Any]:
    """Transform a Model-shaped dict into row column values, ready to persist."""
    row_kwargs = dict(data)
    row_kwargs.pop("id", None)
    for field_name, mode in mapping.credential_fields.items():
        if field_name not in row_kwargs or row_kwargs[field_name] is None:
            continue
        plain = row_kwargs[field_name]
        if mode == "hash":
            row_kwargs[field_name] = hash_value(plain)
        elif mode == "encrypted":
            row_kwargs[field_name] = encrypt_value(plain, resolve_encryption_key())
        else:
            raise ValueError(
                f"Unsupported credential storage mode {mode!r} for field {field_name!r}."
            )
    return row_kwargs


def row_to_model(mapping: EntityMapping, row: object) -> Any:
    """Build a Model instance from a persisted row, applying read-time credential projection."""
    values: dict[str, Any] = {
        column.name: getattr(row, column.name)
        for column in mapping.orm_cls.__table__.columns
    }
    for field_name, mode in mapping.credential_fields.items():
        stored = values.get(field_name)
        if stored is None:
            continue
        if mode == "hash":
            values[field_name] = REDACTED
        elif mode == "encrypted":
            values[field_name] = decrypt_value(stored, resolve_encryption_key())
    return mapping.model_cls.model_validate(values)
