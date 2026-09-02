"""The single error shape of contract v1 and the handlers that render every failure in it."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """The id in the path names no row — answered 404 with code not_found."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(Exception):
    """A body failed validation or referenced an id no row carries — answered 422 with code validation_error."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message)
        self.message = message
        self.field = field


def error_body(code: str, message: str, field: str | None = None) -> dict:
    error: dict = {"code": code, "message": message}
    if field:
        error["field"] = field
    return {"error": error}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def _not_found(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content=error_body("not_found", exc.message))

    @app.exception_handler(ValidationError)
    async def _validation(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content=error_body("validation_error", exc.message, exc.field))

    @app.exception_handler(RequestValidationError)
    async def _request_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        field = None
        message = "Request validation failed"
        if errors:
            first = errors[0]
            loc = [str(part) for part in first.get("loc", ()) if part != "body"]
            field = ".".join(loc) or None
            message = first.get("msg", message)
        return JSONResponse(status_code=422, content=error_body("validation_error", message, field))
