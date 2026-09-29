"""Request identity: a non-secret identifier for every request, and its error-tracking record.

The identifier is generated for each request and never derived from the request. It is returned
in the `X-Request-ID` header of every response and recorded, without the query string or any
header, for every failure that leaves the API.
"""

import logging
import uuid

from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

HEADER = "X-Request-ID"
tracking = logging.getLogger("trading_assistant_api.errors")


def request_id(request: Request) -> str:
    """Return the identifier of a request handled by the API.

    Args:
        request (Request): Request that passed through the request identity middleware.

    Returns:
        (str): The non-secret request identifier.
    """
    return request.state.request_id


def track_failure(
    scope: Scope, identifier: str, status: int, error: BaseException | None
) -> None:
    """Record a failure for error tracking.

    Args:
        scope (Scope): Scope of the failing request.
        identifier (str): The request identifier.
        status (int): Status of the public response.
        error (BaseException, optional): Unexpected failure; only its type is recorded.
    """
    tracking.error(
        "request_id=%s method=%s path=%s status=%s error=%s",
        identifier,
        scope["method"],
        scope["path"],
        status,
        type(error).__name__ if error else "-",
    )


class RequestIdentityMiddleware:
    """Give every HTTP request its identifier, return it, and track every failure."""

    def __init__(self, app: ASGIApp) -> None:
        """Wrap an application.

        Args:
            app (ASGIApp): Application that handles the request.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Handle one ASGI connection."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        identifier = uuid.uuid4().hex
        scope.setdefault("state", {})["request_id"] = identifier
        status = 0

        async def send_with_identifier(message: Message) -> None:
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                MutableHeaders(scope=message)[HEADER] = identifier
            await send(message)

        try:
            await self.app(scope, receive, send_with_identifier)
        except Exception as error:
            track_failure(scope, identifier, 500, error)
            raise
        if status >= 400:
            track_failure(scope, identifier, status, None)
