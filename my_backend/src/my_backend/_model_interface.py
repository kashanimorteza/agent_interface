"""Model Interface: Logic's only route to shared logical Model definitions.

Every domain module Logic needs is imported and re-exported here, from the
Model package's public namespace only. Logic imports from this module, never
directly from ``my_model``.
"""

from __future__ import annotations

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

__all__ = [
    "account",
    "account_group",
    "action",
    "action_group",
    "asset",
    "broker",
    "currency",
    "instance",
    "partial_group",
    "partial_rule",
    "position",
    "trading_platform",
    "trailing_group",
    "trailing_rule",
    "user",
]
