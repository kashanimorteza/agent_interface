"""Insert every mapped entity's declared initial data.

Processes entities in dependency order (my_database._mapping.MAPPINGS is
already ordered so a referenced entity is always seeded first). Safe to run
repeatedly: an initial record already present (matched on its concrete
declared field values) is left untouched rather than duplicated.
"""

from __future__ import annotations

import secrets
from typing import Any

from my_model._initial_data import GENERATE_SECURELY

from my_database import interface
from my_database._mapping import MAPPINGS, EntityMapping


def _resolve_generated_fields(record: dict[str, Any]) -> dict[str, Any]:
    resolved = dict(record)
    for field_name, value in record.items():
        if value is GENERATE_SECURELY:
            resolved[field_name] = secrets.token_urlsafe(32)
    return resolved


def _already_seeded(
    mapping: EntityMapping, record: dict[str, Any], txn: interface.Transaction
) -> bool:
    concrete_filters = {k: v for k, v in record.items() if v is not GENERATE_SECURELY}
    existing = interface.list_(mapping.model_cls, within=txn, **concrete_filters)
    return len(existing) > 0


def seed_all(*, instance: str | None = None) -> int:
    """Seed every declared initial record. Returns the number of records inserted."""
    inserted = 0
    with interface.transaction(instance) as txn:
        for mapping in MAPPINGS:
            for record in getattr(mapping.model_cls, "INITIAL_DATA", ()):
                if _already_seeded(mapping, record, txn):
                    continue
                resolved = _resolve_generated_fields(record)
                candidate = mapping.model_cls.model_validate(resolved)
                interface.add(candidate, within=txn)
                inserted += 1
    return inserted
