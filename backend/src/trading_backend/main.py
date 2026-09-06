"""The Backend application: FastAPI with the Model routers, error mapping, allowed origins, and OpenAPI description."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from trading_backend import __version__
from trading_backend.api.errors import register_error_handlers
from trading_backend.api.routers import ROUTERS

DESCRIPTION = (
    "HTTP API of Trading Assistant. Every shared Model is exposed under /api/<resource> with the standard "
    "operations create, list, get, update, and delete. Credential fields (user.password, user.api_key, "
    "account.password) are write-only: they are accepted on create and update and never returned."
)


def create_app() -> FastAPI:
    """Build the application; settings are read here so importing the module has no other side effect."""
    from trading_backend.settings import get_settings

    settings = get_settings()
    app = FastAPI(
        title="Trading Assistant API",
        version=__version__,
        description=DESCRIPTION,
        openapi_url="/openapi.json",
        docs_url="/docs",
    )
    register_error_handlers(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=False,
    )
    for router in ROUTERS:
        app.include_router(router)
    return app


app = create_app()
