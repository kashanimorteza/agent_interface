"""Inserts every Model-declared initial record, in dependency order, supplying
every system-generated value the Model package intentionally leaves out.
"""

from __future__ import annotations

import secrets

import my_model

from my_database._pipeline import add, list_records

# Dependency order: every referenced Model is seeded before the Model that
# references it. Trailing Rule, Partial Rule, and Position declare no
# initial data and are intentionally absent from this list.
_SEED_ORDER: list[tuple[type[my_model.BaseModel], list[dict[str, object]]]] = [
    (my_model.User, my_model.user.INITIAL_DATA),
    (my_model.TradingPlatform, my_model.trading_platform.INITIAL_DATA),
    (my_model.Instance, my_model.instance.INITIAL_DATA),
    (my_model.Currency, my_model.currency.INITIAL_DATA),
    (my_model.Broker, my_model.broker.INITIAL_DATA),
    (my_model.Asset, my_model.asset.INITIAL_DATA),
    (my_model.AccountGroup, my_model.account_group.INITIAL_DATA),
    (my_model.Account, my_model.account.INITIAL_DATA),
    (my_model.TrailingGroup, my_model.trailing_group.INITIAL_DATA),
    (my_model.PartialGroup, my_model.partial_group.INITIAL_DATA),
    (my_model.ActionGroup, my_model.action_group.INITIAL_DATA),
    (my_model.Action, my_model.action.INITIAL_DATA),
]


def _fill_generated_fields(model_type: type[my_model.BaseModel], record: dict[str, object]) -> dict[str, object]:
    filled = dict(record)
    filled.setdefault("id", 0)  # placeholder; the storage structure assigns the real identity
    for name, field in model_type.model_fields.items():
        extra = field.json_schema_extra
        is_credential = isinstance(extra, dict) and extra.get("credential") is True
        if is_credential and name not in filled:
            filled[name] = secrets.token_urlsafe(24)
    return filled


def seed_initial_data(*, instance: str | None = None) -> dict[str, int]:
    """Seed every declared initial record. Returns the number of records
    inserted per Model name; a Model already holding any record is skipped
    entirely so seeding stays repeatable without duplicating a logical record.
    """

    inserted: dict[str, int] = {}
    for model_type, declared_records in _SEED_ORDER:
        existing = list_records(model_type, limit=1, instance=instance)
        if existing:
            inserted[model_type.__name__] = 0
            continue
        count = 0
        for declared in declared_records:
            filled = _fill_generated_fields(model_type, declared)
            record = model_type(**filled)
            add(record, instance=instance)
            count += 1
        inserted[model_type.__name__] = count
    return inserted
