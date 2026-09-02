"""Entry point — creates the FastAPI application and mounts the routers."""
from fastapi import FastAPI

from app.errors import register_error_handlers

app = FastAPI(
    title="Trading Assistant API",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
)
register_error_handlers(app)
from app.routes import trading_platform as trading_platform_routes  # noqa: E402
app.include_router(trading_platform_routes.router)
from app.routes import broker as broker_routes  # noqa: E402
app.include_router(broker_routes.router)
from app.routes import asset as asset_routes  # noqa: E402
app.include_router(asset_routes.router)
from app.routes import strategy as strategy_routes  # noqa: E402
app.include_router(strategy_routes.router)
from app.routes import trailing_group as trailing_group_routes  # noqa: E402
app.include_router(trailing_group_routes.router)
from app.routes import trailing_rule as trailing_rule_routes  # noqa: E402
app.include_router(trailing_rule_routes.router)
from app.routes import partial_group as partial_group_routes  # noqa: E402
app.include_router(partial_group_routes.router)
from app.routes import partial_rule as partial_rule_routes  # noqa: E402
app.include_router(partial_rule_routes.router)
from app.routes import action_group as action_group_routes  # noqa: E402
app.include_router(action_group_routes.router)
from app.routes import position as position_routes  # noqa: E402
app.include_router(position_routes.router)
