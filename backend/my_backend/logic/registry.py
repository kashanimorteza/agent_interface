"""Where the units are gathered, and nothing more.

This imports the unit each kind of data owns and puts them within reach of the
boundary above. It defines none of them: a unit that lived here instead of in
its own module would have nowhere of its own to become different.
"""

from __future__ import annotations

from typing import Iterator

from my_model import Entity

from ..configuration import Configuration
from ..data_access import DataAccess
from .account import AccountLogic
from .account_group import AccountGroupLogic
from .action import ActionLogic
from .action_group import ActionGroupLogic
from .asset import AssetLogic
from .base import ModelLogic
from .broker import BrokerLogic
from .currency import CurrencyLogic
from .partial_group import PartialGroupLogic
from .partial_rule import PartialRuleLogic
from .position import PositionLogic
from .trading_platform import TradingPlatformLogic
from .trailing_group import TrailingGroupLogic
from .trailing_rule import TrailingRuleLogic
from .user import UserLogic

# One unit per kind of data the project defines, in project order.
UNITS: tuple[type[ModelLogic], ...] = (
    UserLogic,
    CurrencyLogic,
    TradingPlatformLogic,
    BrokerLogic,
    AccountGroupLogic,
    AccountLogic,
    AssetLogic,
    TrailingGroupLogic,
    TrailingRuleLogic,
    PartialGroupLogic,
    PartialRuleLogic,
    ActionGroupLogic,
    ActionLogic,
    PositionLogic,
)


class Behaviour:
    """Every unit, ready to act, keyed by the kind of data it belongs to.

    The route to stored data is opened here rather than handed in, because the
    boundary above has no business holding one: it reaches this, and this
    reaches what is beneath it.
    """

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._data = DataAccess(configuration)
        self._units = {unit.definition.entity_name: unit(self._data) for unit in UNITS}

    def for_definition(self, definition: type[Entity] | str) -> ModelLogic:
        """The unit that owns this kind of data."""

        name = definition if isinstance(definition, str) else definition.entity_name
        if name not in self._units:
            raise KeyError(f"no unit of behaviour belongs to {name!r}")
        return self._units[name]

    def __iter__(self) -> Iterator[ModelLogic]:
        return iter(self._units.values())

    def __len__(self) -> int:
        return len(self._units)

    def close(self) -> None:
        self._data.close()


__all__ = ["UNITS", "Behaviour"]
