"""Seeds every Model-declared initial record, in dependency order and idempotently."""

from __future__ import annotations

import secrets
from typing import Any

import my_model as m

from . import operations
from .transactions import Unit

#: (Model type, natural-key fields) in dependency order. A natural key is the
#: declared uniqueness rule (or, for Trading Platform, its stable ``code``)
#: used to detect a record that was already seeded.
_SEED_ORDER: list[tuple[type[m.BaseModel], tuple[str, ...]]] = [
    (m.User, ("name",)),
    (m.TradingPlatform, ("code",)),
    (m.Currency, ("user_id", "code")),
    (m.Broker, ("user_id", "name")),
    (m.AccountGroup, ("user_id", "name")),
    (m.TrailingGroup, ("user_id", "name")),
    (m.PartialGroup, ("user_id", "name")),
    (m.ActionGroup, ("user_id", "name")),
    (m.Instance, ("user_id", "name")),
    (m.Asset, ("broker_id", "symbol")),
    (m.Account, ("name",)),
    (m.Action, ("action_group_id", "name")),
]


def _resolve_value(value: Any) -> Any:
    if value is m.GENERATE_SECURELY:
        return secrets.token_urlsafe(24)
    return value


def seed_all(*, unit: Unit | None = None, instance: str | None = None) -> dict[str, int]:
    """Insert every declared initial record that does not already exist.

    Returns a count of records actually inserted, keyed by Model name.
    """
    inserted: dict[str, int] = {}
    for model_type, natural_key in _SEED_ORDER:
        count = 0
        for record in model_type.initial_data:
            resolved = {field: _resolve_value(value) for field, value in record.items()}
            criteria = {field: resolved[field] for field in natural_key}
            existing = operations.list(model_type, unit=unit, instance=instance, **criteria)
            if existing:
                continue
            operations.add(model_type, unit=unit, instance=instance, **resolved)
            count += 1
        inserted[model_type.__name__] = count
    return inserted
