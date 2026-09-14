"""Request correlation and safe operational logging (task P3-G12-T2).

Implemented as a raw ASGI middleware rather than `BaseHTTPMiddleware`
(`app.middleware("http")`): that style wraps the exception-handling layer and re-raises
an exception past a registered exception handler before the test client (or a real
server) ever sees the handler's response, defeating Application Outcome mapping for any
request this middleware wraps.
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Awaitable, Callable, MutableMapping

logger = logging.getLogger("backend.requests")

REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_HEADER_BYTES = REQUEST_ID_HEADER.encode("latin-1")
_REQUEST_ID_HEADER_LOWER = _REQUEST_ID_HEADER_BYTES.lower()

Scope = MutableMapping[str, object]
Receive = Callable[[], Awaitable[MutableMapping[str, object]]]
Send = Callable[[MutableMapping[str, object]], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


class RequestCorrelationMiddleware:
    """Attaches a non-secret request identifier to every request's state and response."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        raw_headers: list[tuple[bytes, bytes]] = scope.get("headers", [])  # type: ignore[assignment]
        incoming = next(
            (
                value.decode("latin-1")
                for key, value in raw_headers
                if key.lower() == _REQUEST_ID_HEADER_LOWER
            ),
            None,
        )
        request_id = incoming or uuid.uuid4().hex

        state = scope.setdefault("state", {})
        state["request_id"] = request_id  # type: ignore[index]

        path = scope.get("path", "")
        logger.info("request_started", extra={"request_id": request_id, "request_path": path})

        status_holder: dict[str, int] = {}

        async def send_wrapper(message: MutableMapping[str, object]) -> None:
            if message["type"] == "http.response.start":
                status_holder["status_code"] = message["status"]  # type: ignore[assignment]
                headers = list(message.get("headers", []))  # type: ignore[arg-type]
                headers.append((_REQUEST_ID_HEADER_BYTES, request_id.encode("latin-1")))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_wrapper)

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "request_path": path,
                "status_code": status_holder.get("status_code"),
            },
        )
