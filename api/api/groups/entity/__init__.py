"""Entity Group: Entity Service served as Endpoints, one Adapter for every Entity."""

from fastapi import APIRouter
from logic.interface import Entity

from api.groups.entity import (
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

ROLE = "entity"
NAME = "Entity"
SEGMENT = "entity"
SOURCE = Entity
ADAPTERS: dict[str, APIRouter] = {
    "user": user.router,
    "trading_platform": trading_platform.router,
    "instance": instance.router,
    "currency": currency.router,
    "broker": broker.router,
    "asset": asset.router,
    "account_group": account_group.router,
    "account": account.router,
    "trailing_group": trailing_group.router,
    "trailing_rule": trailing_rule.router,
    "partial_group": partial_group.router,
    "partial_rule": partial_rule.router,
    "action_group": action_group.router,
    "action": action.router,
    "position": position.router,
}
