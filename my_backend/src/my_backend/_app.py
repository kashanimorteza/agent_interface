"""API Interface application composition: one explicit application boundary."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from my_backend.api import (
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

_ROUTERS = (
    user.router,
    trading_platform.router,
    currency.router,
    broker.router,
    instance.router,
    asset.router,
    account_group.router,
    account.router,
    trailing_group.router,
    trailing_rule.router,
    partial_group.router,
    partial_rule.router,
    action_group.router,
    action.router,
    position.router,
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    # No application-wide resources to acquire yet. Present explicitly so
    # future startup/shutdown behavior has one place to live, per the
    # selected API framework's implementation standard.
    yield


def create_app() -> FastAPI:
    """The package's documented public startup boundary."""
    app = FastAPI(
        title="Trading Assistant API",
        description="Backend API Interface for the Trading Assistant.",
        version="0.1.0",
        lifespan=lifespan,
    )
    for router in _ROUTERS:
        app.include_router(router)
    return app
