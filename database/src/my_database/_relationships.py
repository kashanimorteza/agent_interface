"""Relationship targets declared by the project's Target definition.

Model expresses a relationship as a same-record ``*_id`` field naming what it
identifies; it does not itself carry the referenced Model as machine-readable
metadata (see the Model package's ``*_id`` field descriptions). Resolving
that reference to a physical foreign key is Database's own mapping
responsibility, so the target of each relationship field is declared here,
directly from the project's stated Relationships, once per field.
"""

from __future__ import annotations

import my_model as m

RELATIONSHIP_TARGETS: dict[type, dict[str, type]] = {
    m.Instance: {"user_id": m.User, "trading_platform_id": m.TradingPlatform},
    m.Currency: {"user_id": m.User},
    m.Broker: {"user_id": m.User},
    m.Asset: {"broker_id": m.Broker},
    m.AccountGroup: {"user_id": m.User},
    m.Account: {
        "group_id": m.AccountGroup,
        "broker_id": m.Broker,
        "instance_id": m.Instance,
        "base_currency_id": m.Currency,
    },
    m.TrailingGroup: {"user_id": m.User},
    m.TrailingRule: {"trailing_group_id": m.TrailingGroup},
    m.PartialGroup: {"user_id": m.User},
    m.PartialRule: {"partial_group_id": m.PartialGroup},
    m.ActionGroup: {"user_id": m.User},
    m.Action: {
        "action_group_id": m.ActionGroup,
        "asset_id": m.Asset,
        "account_id": m.Account,
        "partial_group_id": m.PartialGroup,
        "trailing_group_id": m.TrailingGroup,
    },
    m.Position: {
        "user_id": m.User,
        "trading_platform_id": m.TradingPlatform,
        "broker_id": m.Broker,
        "account_id": m.Account,
        "trailing_group_id": m.TrailingGroup,
        "partial_group_id": m.PartialGroup,
        "action_group_id": m.ActionGroup,
        "action_id": m.Action,
    },
}

# Every persistent Model, in dependency order (a Model never precedes a Model
# it references), reused for table creation order and initial-data seeding.
PERSISTENT_MODELS: tuple[type, ...] = (
    m.User,
    m.TradingPlatform,
    m.Instance,
    m.Currency,
    m.Broker,
    m.Asset,
    m.AccountGroup,
    m.TrailingGroup,
    m.TrailingRule,
    m.PartialGroup,
    m.PartialRule,
    m.ActionGroup,
    m.Account,
    m.Action,
    m.Position,
)
