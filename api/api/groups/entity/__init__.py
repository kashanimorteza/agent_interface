"""Entity Group.

Group: role entity, name Entity.
Source: Entity Service through Logic Interface; it takes from it the Child Services, their Actions, and the contracts it publishes.
Adapters: one for every Child Service Entity Service presents, bound to that Child Service's Entity.
Endpoints: one for every Action of each Adapter's Child Service.
Parameters: exactly the Action's, with its names, requirements, structures, and defaults.
Handler: calls the same Action on the bound Child Service through the source and returns its result and errors unchanged.
"""

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

routers = (
    account.router,
    account_group.router,
    action.router,
    action_group.router,
    asset.router,
    broker.router,
    currency.router,
    instance.router,
    partial_group.router,
    partial_rule.router,
    position.router,
    trading_platform.router,
    trailing_group.router,
    trailing_rule.router,
    user.router,
)
