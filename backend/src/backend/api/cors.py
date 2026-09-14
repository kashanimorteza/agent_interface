"""CORS allowlist policy (task P3-G10-T4)."""

from __future__ import annotations

from typing import Any


def cors_middleware_kwargs(allowed_origins: list[str]) -> dict[str, Any]:
    """Build starlette CORSMiddleware kwargs enforcing the allowlist policy.

    A wildcard origin is never combined with credentialed access.
    """
    wildcard = "*" in allowed_origins
    return {
        "allow_origins": allowed_origins,
        "allow_credentials": not wildcard,
        "allow_methods": ["GET", "POST", "PUT"],
        "allow_headers": ["X-API-Key", "Content-Type", "X-Request-ID"],
    }
