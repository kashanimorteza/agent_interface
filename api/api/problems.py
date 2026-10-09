"""The mapping of every error an Endpoint returns to RFC 9457 Problem Details."""

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from logic.interface import Entity

database_error = Entity.database_error

STATUS: dict[type, int] = {
    database_error.InvalidInputError: 422,
    database_error.InactiveInstanceError: 503,
    database_error.ConnectionFailureError: 503,
    database_error.ExecutionError: 500,
    database_error.DeclarationMismatchError: 500,
    database_error.ConfigurationError: 500,
}

SERVER_ERROR = 500


def _problem(error: Exception, status: int, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": type(error).__name__,
            "title": HTTPStatus(status).phrase,
            "status": status,
            "detail": detail,
        },
    )


def _status(error: Exception) -> int:
    return next(
        (STATUS[kind] for kind in type(error).__mro__ if kind in STATUS), SERVER_ERROR
    )


async def _database_error(request: Request, error: Exception) -> JSONResponse:
    return _problem(error, _status(error), str(error))


async def _unexpected(request: Request, error: Exception) -> JSONResponse:
    return _problem(error, SERVER_ERROR, "The request could not be completed.")


async def _malformed(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, RequestValidationError)
    where = "; ".join(
        f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}"
        for item in error.errors()
    )
    return _problem(error, 422, where)


def register_problems(app: FastAPI) -> None:
    """Send every error of every Endpoint as Problem Details."""
    app.add_exception_handler(database_error.DatabaseError, _database_error)
    app.add_exception_handler(RequestValidationError, _malformed)
    app.add_exception_handler(Exception, _unexpected)
