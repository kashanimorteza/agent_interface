"""Problems: every error an Endpoint returns is Problem Details with its class name as type."""

from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from logic.interface import Entity
from starlette.exceptions import HTTPException as RoutingError

MEDIA_TYPE = "application/problem+json"
DEFAULT_STATUS = 500
STATUS_BY_ERROR: dict[type[Exception], int] = {
    Entity.Error.InvalidInputError: 422,
    Entity.Error.LifecycleError: 409,
    Entity.Error.InactiveInstanceError: 503,
    Entity.Error.ConnectionFailureError: 503,
}


def status_of(error: Exception) -> int:
    for kind, status in STATUS_BY_ERROR.items():
        if isinstance(error, kind):
            return status
    return DEFAULT_STATUS


def phrase(status: int) -> str:
    try:
        return HTTPStatus(status).phrase
    except ValueError:
        return "Error"


def problem(request: Request, name: str, status: int, detail: str) -> JSONResponse:
    body = {
        "type": name,
        "title": phrase(status),
        "status": status,
        "detail": detail,
        "instance": request.url.path,
    }
    return JSONResponse(body, status_code=status, media_type=MEDIA_TYPE)


async def database_error(request: Request, error: Exception) -> JSONResponse:
    return problem(request, type(error).__name__, status_of(error), str(error))


async def request_error(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, RequestValidationError)
    reasons = "; ".join(
        f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}" for item in error.errors()
    )
    name = Entity.Error.InvalidInputError.__name__
    return problem(request, name, STATUS_BY_ERROR[Entity.Error.InvalidInputError], reasons)


async def routing_error(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, RoutingError)
    return problem(request, type(error).__name__, error.status_code, str(error.detail))


async def unexpected_error(request: Request, error: Exception) -> JSONResponse:
    return problem(
        request, type(error).__name__, DEFAULT_STATUS, "The request could not be served."
    )


def register(api: FastAPI) -> None:
    handlers: list[tuple[Any, Any]] = [
        (Entity.Error.DatabaseError, database_error),
        (RequestValidationError, request_error),
        (RoutingError, routing_error),
        (Exception, unexpected_error),
    ]
    for kind, handler in handlers:
        api.add_exception_handler(kind, handler)
