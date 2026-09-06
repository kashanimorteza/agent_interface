"""The registry of shared Models and the accessor for their definitions."""

from functools import lru_cache
from types import MappingProxyType
from typing import Mapping

from ._base import Model, build_spec
from ._spec import ModelSpec
from .account import Account
from .account_group import AccountGroup
from .action import Action
from .action_group import ActionGroup
from .asset import Asset
from .broker import Broker
from .currency import Currency
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import User

MODELS: Mapping[str, type[Model]] = MappingProxyType(
    {
        "user": User,
        "currency": Currency,
        "trading_platform": TradingPlatform,
        "broker": Broker,
        "account_group": AccountGroup,
        "account": Account,
        "asset": Asset,
        "trailing_group": TrailingGroup,
        "trailing_rule": TrailingRule,
        "partial_group": PartialGroup,
        "partial_rule": PartialRule,
        "action_group": ActionGroup,
        "action": Action,
        "position": Position,
    }
)
"""Every shared Model, keyed by its Model key in project order."""


@lru_cache(maxsize=None)
def _spec_of(model: type[Model]) -> ModelSpec:
    return build_spec(model)


def model_metadata(model: type[Model] | Model) -> ModelSpec:
    """Return the resolved logical definition of a shared Model.

    Accepts a Model class or an instance of one, and returns its key, purpose,
    fields in declared order with their properties, relationships, rules, and
    initial data. Raises LookupError for anything that is not a shared Model.
    """
    resolved = model if isinstance(model, type) else type(model)
    if resolved not in MODELS.values():
        raise LookupError(f"{resolved.__qualname__} is not a shared Model")
    return _spec_of(resolved)
