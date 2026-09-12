"""Registry connecting each Model type to its persistence mapping.

Credential fields and the uniqueness rule are read directly from the
Model's own declared metadata (JSON schema `credential`/`storage_at_rest`,
and `UNIQUE_TOGETHER`) rather than re-declared here, so Database never
maintains a second, competing definition of Model-owned meaning.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from my_model import (
    account,
    account_group,
    action,
    action_group,
    asset,
    broker,
    currency,
    instance,
    partial_group,
    partial_rule,
    position,
    trading_platform,
    trailing_group,
    trailing_rule,
    user,
)
from my_model._base import BaseModel

from my_database import _orm
from my_database._base import Base


@dataclass(frozen=True)
class EntityMapping:
    model_cls: type[BaseModel]
    orm_cls: type[Base]
    credential_fields: dict[str, str] = field(default_factory=dict)
    unique_together: tuple[tuple[str, ...], ...] = ()


def _credential_fields(model_cls: type[BaseModel]) -> dict[str, str]:
    schema = model_cls.model_json_schema()
    result: dict[str, str] = {}
    for name, spec in schema.get("properties", {}).items():
        if isinstance(spec, dict) and spec.get("credential") is True:
            result[name] = spec.get("storage_at_rest", "hash")
    return result


def _mapping(model_cls: type[BaseModel], orm_cls: type[Base]) -> EntityMapping:
    return EntityMapping(
        model_cls=model_cls,
        orm_cls=orm_cls,
        credential_fields=_credential_fields(model_cls),
        unique_together=getattr(model_cls, "UNIQUE_TOGETHER", ()),
    )


# Dependency order: an entity appears after every entity it references.
MAPPINGS: tuple[EntityMapping, ...] = (
    _mapping(user.User, _orm.UserRow),
    _mapping(trading_platform.TradingPlatform, _orm.TradingPlatformRow),
    _mapping(currency.Currency, _orm.CurrencyRow),
    _mapping(broker.Broker, _orm.BrokerRow),
    _mapping(instance.Instance, _orm.InstanceRow),
    _mapping(asset.Asset, _orm.AssetRow),
    _mapping(account_group.AccountGroup, _orm.AccountGroupRow),
    _mapping(account.Account, _orm.AccountRow),
    _mapping(trailing_group.TrailingGroup, _orm.TrailingGroupRow),
    _mapping(trailing_rule.TrailingRule, _orm.TrailingRuleRow),
    _mapping(partial_group.PartialGroup, _orm.PartialGroupRow),
    _mapping(partial_rule.PartialRule, _orm.PartialRuleRow),
    _mapping(action_group.ActionGroup, _orm.ActionGroupRow),
    _mapping(action.Action, _orm.ActionRow),
    _mapping(position.Position, _orm.PositionRow),
)

_BY_MODEL: dict[type[BaseModel], EntityMapping] = {m.model_cls: m for m in MAPPINGS}


class UnmappedModelError(LookupError):
    def __init__(self, model_cls: object) -> None:
        super().__init__(f"{model_cls!r} has no Database mapping.")


def mapping_for(model_cls: type[BaseModel]) -> EntityMapping:
    try:
        return _BY_MODEL[model_cls]
    except KeyError as exc:
        raise UnmappedModelError(model_cls) from exc
