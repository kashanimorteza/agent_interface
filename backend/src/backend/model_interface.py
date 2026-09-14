"""Backend's Model Interface (task P3-G1-T1): the sole route through which Logic and API
Interface reach Model's Public Interface. Nothing here redefines a Domain Definition;
every name below is re-exported directly from `model`.
"""

from __future__ import annotations

from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    ModelBase,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)

__all__ = [
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Currency",
    "Instance",
    "ModelBase",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]

DOMAIN_DEFINITIONS: tuple[type[ModelBase], ...] = (
    User,
    TradingPlatform,
    Instance,
    Currency,
    Broker,
    Asset,
    AccountGroup,
    Account,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)
"""Every Domain Definition Backend operates on, in dependency order."""
