"""Entity Group: one Adapter for every Entity Child Service that Entity Service presents."""

from fastapi import APIRouter
from fastapi.routing import APIRoute

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

NAME = "Entity"
_adapters = (
    user,
    trading_platform,
    instance,
    currency,
    broker,
    asset,
    account_group,
    account,
    trailing_group,
    trailing_rule,
    partial_group,
    partial_rule,
    action_group,
    action,
    position,
)

_identities = [
    (method, route.path)
    for adapter in _adapters
    for route in adapter.router.routes
    if isinstance(route, APIRoute)
    for method in route.methods or ()
]
if len(_identities) != len(set(_identities)):
    raise ValueError(
        "Entity Group Endpoints must have unique Method-and-Path combinations"
    )

router = APIRouter()
for adapter in _adapters:
    router.include_router(adapter.router)
