"""One Logic unit per shared Model.

Every unit inherits the standard baseline; Model-specific Behaviour is empty for every Model in this
phase, exactly as resolved in the generated Backend configuration.
"""

from __future__ import annotations

from typing import Any

from trading_backend.errors import UnknownModelError
from trading_backend.logic.model_logic import ModelLogic


class UserLogic(ModelLogic):
    model = "user"


class CurrencyLogic(ModelLogic):
    model = "currency"


class TradingPlatformLogic(ModelLogic):
    model = "trading_platform"


class BrokerLogic(ModelLogic):
    model = "broker"


class AccountLogic(ModelLogic):
    model = "account"


class AssetLogic(ModelLogic):
    model = "asset"


class TrailingGroupLogic(ModelLogic):
    model = "trailing_group"


class TrailingRuleLogic(ModelLogic):
    model = "trailing_rule"


class PartialGroupLogic(ModelLogic):
    model = "partial_group"


class PartialRuleLogic(ModelLogic):
    model = "partial_rule"


class ActionGroupLogic(ModelLogic):
    model = "action_group"


class ActionLogic(ModelLogic):
    model = "action"


class PositionLogic(ModelLogic):
    model = "position"


MODEL_LOGIC: dict[str, type[ModelLogic]] = {
    unit.model: unit
    for unit in (
        UserLogic,
        CurrencyLogic,
        TradingPlatformLogic,
        BrokerLogic,
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
}


def get_logic(model: str, data_access: Any) -> ModelLogic:
    """The Logic unit of ``model`` bound to ``data_access``, or UnknownModelError."""
    try:
        unit = MODEL_LOGIC[model]
    except KeyError:
        raise UnknownModelError(f"unknown Model {model!r}; known Models: {', '.join(MODEL_LOGIC)}") from None
    return unit(data_access)
