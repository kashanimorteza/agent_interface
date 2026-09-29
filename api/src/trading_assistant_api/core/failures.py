"""Public representation of failures: safe when unexpected, faithful when declared.

Every failure body is `{"detail": ..., "request_id": ...}`. An unexpected failure exposes no
exception, persistence detail, or secret. A declared failure names the rule that was not met,
and a missing record is a failure of its own, so neither can be mistaken for a success. Input
that violates an Endpoint's published shape is refused before it reaches the Adapter; the refusal
names the input and the rule and never repeats what the caller supplied.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from trading_assistant_api.core.requests import HEADER, request_id


class FailureBody(BaseModel):
    """The public body of every failure.

    Attributes:
        detail (str): The rule that was not met, free of secrets.
        request_id (str): The non-secret identifier of the failed request.
    """

    detail: str
    request_id: str


class DeclaredFailure(Exception):
    """A request an Action refused; `detail` names the rule that was not met."""

    def __init__(self, detail: str) -> None:
        """Keep the refusal.

        Args:
            detail (str): The rule that was not met, free of secrets.
        """
        super().__init__(detail)
        self.detail = detail


class RecordNotFound(Exception):
    """A request named a record that does not exist."""


def _failure(request: Request, status: int, detail: str) -> JSONResponse:
    """Build the public failure response carrying the request identifier."""
    identifier = request_id(request)
    return JSONResponse(
        {"detail": detail, "request_id": identifier},
        status_code=status,
        headers={HEADER: identifier},
    )


async def _declared(request: Request, error: Exception) -> JSONResponse:
    """Represent a refusal declared by an Action."""
    assert isinstance(error, DeclaredFailure)
    return _failure(request, 409, error.detail)


async def _missing(request: Request, error: Exception) -> JSONResponse:
    """Represent a request that named a record which does not exist."""
    return _failure(request, 404, "No record has the requested id")


async def _invalid(request: Request, error: Exception) -> JSONResponse:
    """Represent input that violates an Endpoint's published shape, without repeating it."""
    assert isinstance(error, RequestValidationError)
    detail = "; ".join(
        f"{'.'.join(map(str, problem['loc']))}: {problem['msg']}"
        for problem in error.errors()
    )
    return _failure(request, 422, detail)


async def _refused(request: Request, error: Exception) -> JSONResponse:
    """Represent a request no route serves, such as an unknown path or a wrong method."""
    assert isinstance(error, HTTPException)
    return _failure(request, error.status_code, str(error.detail))


async def _unexpected(request: Request, error: Exception) -> JSONResponse:
    """Represent a failure no Action declares, revealing nothing internal."""
    return _failure(request, 500, "Internal server error")


def install_failure_handlers(app: FastAPI) -> None:
    """Register the public failure representations on the application.

    Args:
        app (FastAPI): Application whose failures are represented.
    """
    app.add_exception_handler(DeclaredFailure, _declared)
    app.add_exception_handler(RecordNotFound, _missing)
    app.add_exception_handler(RequestValidationError, _invalid)
    app.add_exception_handler(HTTPException, _refused)
    app.add_exception_handler(Exception, _unexpected)
