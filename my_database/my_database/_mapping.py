"""Resolves the persistence mapping between a public Model type and its
internal ORM row class, and applies each Model-declared credential field's
storage transformation on write and its reverse (or redaction) on read.

An explicit Model-declared storage mode always takes precedence over any of
Database's own generic field-name defaults.
"""

from __future__ import annotations

from typing import Any

import my_model

from my_database import _orm
from my_database._credentials import REDACTED, decrypt_value, encrypt_value, hash_value

MODEL_TO_ORM: dict[type[my_model.BaseModel], type[_orm.Base]] = {
    my_model.User: _orm.UserRow,
    my_model.TradingPlatform: _orm.TradingPlatformRow,
    my_model.Instance: _orm.InstanceRow,
    my_model.Currency: _orm.CurrencyRow,
    my_model.Broker: _orm.BrokerRow,
    my_model.Asset: _orm.AssetRow,
    my_model.AccountGroup: _orm.AccountGroupRow,
    my_model.Account: _orm.AccountRow,
    my_model.TrailingGroup: _orm.TrailingGroupRow,
    my_model.TrailingRule: _orm.TrailingRuleRow,
    my_model.PartialGroup: _orm.PartialGroupRow,
    my_model.PartialRule: _orm.PartialRuleRow,
    my_model.ActionGroup: _orm.ActionGroupRow,
    my_model.Action: _orm.ActionRow,
    my_model.Position: _orm.PositionRow,
}


def resolve_orm_type(model_type: type[my_model.BaseModel]) -> type[_orm.Base]:
    try:
        return MODEL_TO_ORM[model_type]
    except KeyError as error:
        raise LookupError(f"{model_type!r} has no registered persistence mapping.") from error


def credential_fields(model_type: type[my_model.BaseModel]) -> dict[str, str]:
    """Field name -> declared storage_at_rest ("hash" | "encrypted") for
    every field the Model itself declares as a credential.
    """

    result: dict[str, str] = {}
    for name, field in model_type.model_fields.items():
        extra = field.json_schema_extra
        if isinstance(extra, dict) and extra.get("credential") is True:
            result[name] = str(extra["storage_at_rest"])
    return result


def apply_write_transform(model_type: type[my_model.BaseModel], values: dict[str, Any]) -> dict[str, Any]:
    """Transform declared credential fields present in ``values`` for storage."""

    transformed = dict(values)
    for name, mode in credential_fields(model_type).items():
        raw = transformed.get(name)
        if raw is None:
            continue
        transformed[name] = hash_value(raw) if mode == "hash" else encrypt_value(raw)
    return transformed


def apply_read_transform(model_type: type[my_model.BaseModel], values: dict[str, Any]) -> dict[str, Any]:
    """Reverse declared credential fields present in ``values`` after a read:
    a hash is irreversible and becomes the redacted marker; an encrypted
    value is decrypted back to its original, recoverable meaning.
    """

    transformed = dict(values)
    for name, mode in credential_fields(model_type).items():
        stored = transformed.get(name)
        if stored is None:
            continue
        transformed[name] = REDACTED if mode == "hash" else decrypt_value(stored)
    return transformed


def row_to_model[T: my_model.BaseModel](model_type: type[T], row: _orm.Base) -> T:
    values = {name: getattr(row, name) for name in model_type.model_fields}
    return model_type(**apply_read_transform(model_type, values))
