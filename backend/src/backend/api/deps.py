"""FastAPI dependency wiring: Database access, request correlation, authentication."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, Request

from ..database_interface import DatabaseInterface
from ..logic.auth import authenticate
from ..request_context import RequestContext


def get_database_interface(request: Request) -> DatabaseInterface:
    return request.app.state.database_interface


DatabaseInterfaceDep = Annotated[DatabaseInterface, Depends(get_database_interface)]


def get_request_id(request: Request) -> str:
    return request.state.request_id


RequestIdDep = Annotated[str, Depends(get_request_id)]


def get_authenticated_context(
    db: DatabaseInterfaceDep,
    request_id: RequestIdDep,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> RequestContext:
    return authenticate(db, x_api_key, request_id=request_id)


AuthenticatedContextDep = Annotated[RequestContext, Depends(get_authenticated_context)]
