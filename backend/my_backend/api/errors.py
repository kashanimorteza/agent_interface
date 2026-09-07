"""Mapping of logical outcomes to external responses.

Every error body describes the failure without carrying the offending input,
which may be a credential, and without carrying a persistence detail.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..outcomes import ConflictingRecord, InvalidData, NoLogicUnit, RecordNotFound

SAFE_ERROR_KEYS = ("type", "loc", "msg")


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def transport_shape(_: Request, exc: RequestValidationError) -> JSONResponse:
        detail = [{k: v for k, v in error.items() if k in SAFE_ERROR_KEYS} for error in exc.errors()]
        return JSONResponse(status_code=422, content={"detail": detail})

    @app.exception_handler(InvalidData)
    async def invalid_data(_: Request, exc: InvalidData) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.errors})

    @app.exception_handler(RecordNotFound)
    async def not_found(_: Request, exc: RecordNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ConflictingRecord)
    async def conflict(_: Request, exc: ConflictingRecord) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(NoLogicUnit)
    async def no_unit(_: Request, exc: NoLogicUnit) -> JSONResponse:
        return JSONResponse(status_code=501, content={"detail": str(exc)})
