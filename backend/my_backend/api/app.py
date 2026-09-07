"""The application: every router, the outcome mapping, and the description."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from my_database import Database
from my_model import MODELS

from ..data_access import DataAccess
from ..logic import build_registry
from ..runtime import BackendSettings, resolve_settings
from .errors import install_error_handlers
from .routes import router_for

TITLE = "Trading Assistant API"
DESCRIPTION = "Enter and manage every defined Model of the Trading Assistant."
DESCRIPTION_PATH = "/openapi.json"
DOCS_PATH = "/docs"


def create_app(settings: BackendSettings | None = None, database: Database | None = None) -> FastAPI:
    """Build the application from the Backend section of the runtime configuration."""
    settings = settings or resolve_settings()
    data_access = DataAccess(settings, database)
    registry = build_registry(data_access)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield
        data_access.close()

    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version="0.1.0",
        openapi_url=DESCRIPTION_PATH if settings.api_documentation else None,
        docs_url=DOCS_PATH if settings.api_documentation else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.settings = settings
    install_error_handlers(app)
    for model in MODELS:
        app.include_router(router_for(model, registry))
    return app
