"""Lifecycle signals: health and readiness, distinct and never disabled.

Both signals are served by the API itself, not by any Group, and are left out of the contract of
Group Endpoints. Health reports that the process is alive; nothing else influences it. Readiness
is positive only while the API has started, with its runtime values already validated, and the
dependency it can observe through its declared connection, Logic's published surface, is there.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from logic import interface as logic


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Mark the API started while it serves and not started once it stops.

    Args:
        app (FastAPI): Application whose readiness follows its lifetime.
    """
    app.state.started = True
    yield
    app.state.started = False


def dependencies_ready() -> bool:
    """Return whether Logic's published surface, the API's only dependency, is available.

    Returns:
        (bool): True when Logic Interface publishes its Entity Service.
    """
    try:
        return bool(logic.Entity.__all__)
    except AttributeError:
        return False


def install_health(app: FastAPI, path: str) -> None:
    """Serve the health signal.

    Args:
        app (FastAPI): Application that serves the signal.
        path (str): Location of the signal.
    """

    @app.get(path, include_in_schema=False)
    def health() -> dict[str, str]:
        return {"status": "alive"}


def install_readiness(app: FastAPI, path: str) -> None:
    """Serve the readiness signal, distinct from health.

    Args:
        app (FastAPI): Application that serves the signal.
        path (str): Location of the signal.
    """
    app.state.started = False

    @app.get(path, include_in_schema=False)
    def readiness() -> JSONResponse:
        ready = app.state.started and dependencies_ready()
        return JSONResponse(
            {"status": "ready" if ready else "not ready"},
            status_code=200 if ready else 503,
        )
