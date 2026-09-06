"""HTTP error mapping.

Backend errors become JSON responses with the mapped status code, and request validation errors are
rewritten without the framework's default echo of the submitted input, so credential values never
appear in an error payload.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from trading_backend.errors import (
    BackendError,
    ConflictError,
    InvalidFieldError,
    NotFoundError,
    UnknownModelError,
    UnsupportedActionError,
)

STATUS_CODES: dict[type[BackendError], int] = {
    NotFoundError: 404,
    ConflictError: 409,
    InvalidFieldError: 422,
    UnsupportedActionError: 400,
    UnknownModelError: 500,
    BackendError: 500,
}


def _handler_for(status_code: int):
    def handle(_request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(exc)})

    return handle


def _validation_handler(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    detail = [{"loc": list(e.get("loc", ())), "msg": e.get("msg", ""), "type": e.get("type", "")} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": detail})


def register_error_handlers(app: FastAPI) -> None:
    """Attach the Backend error mapping and the credential-safe validation handler to ``app``."""
    for exc_class, status_code in STATUS_CODES.items():
        app.add_exception_handler(exc_class, _handler_for(status_code))
    app.add_exception_handler(RequestValidationError, _validation_handler)
