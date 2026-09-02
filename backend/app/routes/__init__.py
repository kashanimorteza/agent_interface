from fastapi import APIRouter

from app.routes import (
    trading_platform,
    broker,
    account,
    asset,
    strategy,
    trailing_group,
    trailing_rule,
    partial_group,
    partial_rule,
    action_group,
    action,
    execute,
    position,
)

router = APIRouter()
for module in (trading_platform, broker, account, asset, strategy, trailing_group, trailing_rule, partial_group, partial_rule, action_group, action, execute, position):
    router.include_router(module.router)
