"""Bootstrap: the single composition and startup point of the API.

It assembles the one running boundary, applies the shared request identity and failure
representation, and starts serving only after every runtime value has been validated. It holds
no Group Action, application Behaviour, or persistence work.
"""

from collections.abc import Collection
from types import ModuleType

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic import interface as logic

from trading_assistant_api.core.configuration import Settings, load_settings
from trading_assistant_api.core.contract import DESCRIPTION, TITLE, VERSION
from trading_assistant_api.core.endpoints import validate_endpoints
from trading_assistant_api.core.failures import install_failure_handlers
from trading_assistant_api.core.lifecycle import (
    install_health,
    install_readiness,
    lifespan,
)
from trading_assistant_api.core.requests import RequestIdentityMiddleware
from trading_assistant_api.groups import GROUPS


def register_groups(
    app: FastAPI,
    groups: tuple[ModuleType, ...] = GROUPS,
    published: Collection[str] = tuple(logic.__all__),
) -> None:
    """Register every generated Group on the one application.

    Args:
        app (FastAPI): The application every Group is served by; no Group starts a server. Every
            Group is served under the one declared version, by path prefix.
        groups (tuple[ModuleType, ...]): The generated Groups.
        published (Collection[str]): Services Logic Interface publishes.

    Raises:
        RuntimeError: When a Group's Service is not published by Logic Interface.
        InvalidRoutes: When a Group identity or a final route is invalid or collides.
    """
    generated = []
    for group in groups:
        if group.SERVICE not in published:
            raise RuntimeError(
                f"Group {group.GROUP} corresponds to Service {group.SERVICE}, "
                "which Logic Interface does not publish"
            )
        generated.append((group, group.endpoints()))
    validate_endpoints(
        VERSION,
        [endpoint for _, endpoints in generated for endpoint in endpoints],
    )
    versioned = APIRouter(prefix=f"/{VERSION}")
    for group, endpoints in generated:
        versioned.include_router(group.build(endpoints))
    app.include_router(versioned)


def create_app(settings: Settings) -> FastAPI:
    """Compose the API's shared boundary.

    Args:
        settings (Settings): Validated runtime values.

    Returns:
        (FastAPI): The one application every Group registers on.
    """
    app = FastAPI(
        title=TITLE,
        description=DESCRIPTION,
        version=VERSION,
        lifespan=lifespan,
        swagger_ui_oauth2_redirect_url=None,
    )
    app.add_middleware(RequestIdentityMiddleware)
    if settings.cors_allowed_origins:
        app.add_middleware(
            CORSMiddleware, allow_origins=list(settings.cors_allowed_origins)
        )
    install_failure_handlers(app)
    install_health(app, settings.health_path)
    install_readiness(app, settings.readiness_path)
    register_groups(app)
    return app


def main() -> None:
    """Validate the runtime values, then serve the API at the declared address."""
    settings = load_settings()
    uvicorn.run(
        create_app(settings),
        host=settings.host,
        port=settings.port,
        timeout_graceful_shutdown=settings.shutdown_timeout_seconds,
    )
