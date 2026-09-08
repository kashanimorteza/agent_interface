"""The contract, assembled and served.

This is where the layer meets the outside world: it builds the routers, decides
how a refusal from beneath becomes a response, and publishes the description of
everything it offers. What the application does is elsewhere, and this file
would be the wrong place to change any of it.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from ..configuration import Configuration, load
from ..faults import BackendFault, Conflict, Invalid, Misconfigured, NotFound, Unsupported
from ..logic import Behaviour
from .routes import routers

TITLE = "Trading Assistant"
SUMMARY = "Enter and manage the data the platform is built from."

# Which kind of refusal becomes which kind of answer. This mapping is the only
# place in the layer that knows an outcome has a number.
ANSWERS: dict[type[BackendFault], int] = {
    NotFound: 404,
    Invalid: 422,
    Conflict: 409,
    Unsupported: 400,
    Misconfigured: 500,
}


def answer_for(fault: BackendFault) -> int:
    for kind, code in ANSWERS.items():
        if isinstance(fault, kind):
            return code
    return 400


def create_app(configuration: Configuration | None = None) -> FastAPI:
    """Build the application from the settings and bindings it was given."""

    settings = configuration or load()
    behaviour = Behaviour(settings)
    described = settings.description

    application = FastAPI(
        title=TITLE,
        summary=SUMMARY,
        version="0.1.0",
        openapi_url=described.path if described.enabled else None,
        docs_url=described.human_readable_path if described.enabled else None,
        redoc_url=None,
    )

    @application.exception_handler(BackendFault)
    def refused(request: Request, fault: BackendFault) -> JSONResponse:
        """A refusal from beneath, said in the transport's own terms.

        The reason travels; nothing that was rejected does, so a refusal about a
        credential never carries the credential.
        """

        return JSONResponse(
            status_code=answer_for(fault),
            content={"refused": type(fault).__name__, "reason": str(fault)},
        )

    @application.get("/health", tags=["service"], summary="Whether the layer is answering")
    def health() -> dict[str, str]:
        return {"status": "ready"}

    for router in routers(behaviour, settings.listing):
        application.include_router(router)

    application.state.behaviour = behaviour
    application.state.configuration = settings
    return application


app = create_app()


__all__ = ["ANSWERS", "answer_for", "app", "create_app"]
