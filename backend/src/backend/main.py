"""Backend's official executable entry point (verified whole by task P3-G13-T1)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from database import Database
from database.runtime_config import RuntimeConfig
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.cors import cors_middleware_kwargs
from .api.errors import register_exception_handlers
from .api.health import router as health_router
from .api.observability import RequestCorrelationMiddleware
from .api.routers import build_all_routers
from .config import Settings, load_settings
from .database_interface import DatabaseInterface


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings: Settings = app.state.settings
    database_config: RuntimeConfig | None = getattr(app.state, "database_config", None)
    db = Database(database_config, instance=settings.database_instance)
    database_interface = DatabaseInterface(
        db,
        timeout_seconds=settings.request_timeout_seconds,
        max_retry_attempts=settings.max_retry_attempts,
    )
    app.state.database_interface = database_interface
    app.state.ready = True
    try:
        yield
    finally:
        app.state.ready = False
        database_interface.close()


def create_app(
    settings: Settings | None = None, *, database_config: RuntimeConfig | None = None
) -> FastAPI:
    """Construct the Backend application. The supported application construction surface
    for verification (task P3-G13-T1): tests build the app only through this function.

    `database_config` lets a caller (tests) point Backend at an isolated RuntimeConfig
    instead of Database's default resolution; production leaves it unset.
    """
    resolved_settings = settings or load_settings()

    app = FastAPI(
        title="Trading Assistant Backend",
        version=resolved_settings.api_version,
        lifespan=lifespan,
    )
    app.state.settings = resolved_settings
    app.state.database_config = database_config
    app.state.ready = False

    app.add_middleware(RequestCorrelationMiddleware)
    app.add_middleware(
        CORSMiddleware, **cors_middleware_kwargs(resolved_settings.cors_allowed_origins)
    )

    register_exception_handlers(app)

    app.include_router(health_router)
    for router in build_all_routers(prefix=f"/{resolved_settings.api_version}"):
        app.include_router(router)

    return app


app = create_app()
"""The official executable entry point Platform starts Backend through."""
