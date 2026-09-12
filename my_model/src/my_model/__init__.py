"""Public interface of the my_model package.

The independent, platform-independent logical Model shared by every
technical component. Consumers use either:

    import my_model
    my_model.user.User(...)

or:

    from my_model import user
    user.User(...)

Every public module listed here is part of the documented interface;
internal modules such as ``_base`` and ``_unique`` are not.
"""

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
