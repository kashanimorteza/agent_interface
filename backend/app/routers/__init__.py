from fastapi import APIRouter

from app.routers import (
    account,
    action,
    action_group,
    asset,
    broker,
    execute,
    partial_group,
    partial_rule,
    position,
    strategy,
    trading_platform,
    trailing_group,
    trailing_rule,
)

router = APIRouter()

# Register each model router's concrete routes on the aggregate router so
# `router.routes` lists every contract route directly (FastAPI's include_router
# would otherwise defer them behind a lazy _IncludedRouter entry).
for _module in (
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
):
    router.routes.extend(_module.router.routes)
