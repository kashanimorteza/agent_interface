"""Application Outcome and unexpected-failure mapping (task P3-G11-T1)."""

from __future__ import annotations

import logging

from database import ConstraintViolation
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..database_interface import PersistenceTimeout
from ..logic.outcomes import (
    ApplicationOutcome,
    ConflictOutcome,
    NotFound,
    Unauthenticated,
    Unauthorized,
    ValidationFailed,
)

logger = logging.getLogger("backend.errors")

_OUTCOME_STATUS: dict[type[ApplicationOutcome], int] = {
    NotFound: status.HTTP_404_NOT_FOUND,
    ValidationFailed: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ConflictOutcome: status.HTTP_409_CONFLICT,
    Unauthenticated: status.HTTP_401_UNAUTHORIZED,
    Unauthorized: status.HTTP_403_FORBIDDEN,
}


def _request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


async def application_outcome_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ApplicationOutcome)
    status_code = _OUTCOME_STATUS.get(type(exc), status.HTTP_400_BAD_REQUEST)
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc), "request_id": _request_id(request)},
    )


async def constraint_violation_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ConstraintViolation)
    return await application_outcome_handler(request, ConflictOutcome(str(exc)))


async def unexpected_failure_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = _request_id(request)
    logger.error(
        "unexpected_failure", extra={"request_id": request_id, "error_type": type(exc).__name__}
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred.", "request_id": request_id},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationOutcome, application_outcome_handler)
    app.add_exception_handler(ConstraintViolation, constraint_violation_handler)
    app.add_exception_handler(PersistenceTimeout, unexpected_failure_handler)
    app.add_exception_handler(Exception, unexpected_failure_handler)
