"""The Backend HTTP API application: converts logical outcomes raised by
Logic and Database Interface into distinguishable protocol outcomes.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from my_backend import _database_interface as db
from my_backend._errors import BackendLogicError
from my_backend.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Trading Assistant Backend",
        description="Application Behaviour and public HTTP API for the Trading Assistant Target.",
    )
    app.include_router(api_router)

    @app.exception_handler(db.NotFoundError)
    def _not_found(_request: Request, exc: db.NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(db.ConstraintViolationError)
    def _constraint_violation(_request: Request, exc: db.ConstraintViolationError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(db.StatusNotSupportedError)
    def _status_not_supported(_request: Request, exc: db.StatusNotSupportedError) -> JSONResponse:
        return JSONResponse(status_code=405, content={"detail": str(exc)})

    @app.exception_handler(db.TransactionConflictError)
    def _transaction_conflict(_request: Request, exc: db.TransactionConflictError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(BackendLogicError)
    def _backend_logic_error(_request: Request, exc: BackendLogicError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    def _model_validation_error(_request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.errors(include_url=False)})

    return app


app = create_app()
