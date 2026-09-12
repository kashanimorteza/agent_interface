"""API Interface: the only external boundary through which Logic is reached.

Builds one router per Model Logic unit and aggregates them under one
top-level router. Routing paths, methods, and file organization are
implementation decisions; the Backend Preferences require only that every
standard operation each Model supports is exposed. Model types reach this
layer only through the Model Logic unit that owns each one, never through a
direct Model import.
"""

from typing import Any

from fastapi import APIRouter

from my_backend import logic
from my_backend.api._factory import build_router
from my_backend.logic._base import ModelLogic

router = APIRouter()

_ROUTES: list[tuple[ModelLogic[Any], str, str]] = [
    (logic.user.logic, "/users", "users"),
    (logic.trading_platform.logic, "/trading-platforms", "trading-platforms"),
    (logic.instance.logic, "/instances", "instances"),
    (logic.currency.logic, "/currencies", "currencies"),
    (logic.broker.logic, "/brokers", "brokers"),
    (logic.asset.logic, "/assets", "assets"),
    (logic.account_group.logic, "/account-groups", "account-groups"),
    (logic.account.logic, "/accounts", "accounts"),
    (logic.trailing_group.logic, "/trailing-groups", "trailing-groups"),
    (logic.trailing_rule.logic, "/trailing-rules", "trailing-rules"),
    (logic.partial_group.logic, "/partial-groups", "partial-groups"),
    (logic.partial_rule.logic, "/partial-rules", "partial-rules"),
    (logic.action_group.logic, "/action-groups", "action-groups"),
    (logic.action.logic, "/actions", "actions"),
    (logic.position.logic, "/positions", "positions"),
]

for _model_logic, _prefix, _tag in _ROUTES:
    router.include_router(build_router(_model_logic, prefix=_prefix, tag=_tag))
