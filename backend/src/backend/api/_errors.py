"""Maps Data Access failure types to HTTP responses. API owns no Behaviour;
this only translates an already-decided outcome into a transport response.
"""

from __future__ import annotations

from fastapi import HTTPException

from .. import data_access


def to_http(error: Exception) -> HTTPException:
    if isinstance(error, data_access.NotFound):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, data_access.ValidationFailed):
        return HTTPException(status_code=422, detail=str(error))
    if isinstance(error, data_access.ConstraintViolation):
        return HTTPException(status_code=409, detail=str(error))
    if isinstance(error, data_access.UnsupportedOperation):
        return HTTPException(status_code=405, detail=str(error))
    return HTTPException(status_code=500, detail="internal error")
