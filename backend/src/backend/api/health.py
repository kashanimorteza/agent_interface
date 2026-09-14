"""Health and readiness signals (task P3-G12-T1)."""

from __future__ import annotations

from fastapi import APIRouter, Request, Response, status

router = APIRouter(tags=["lifecycle"])


@router.get("/health")
def health() -> dict[str, str]:
    """Reports that the process is running, independent of dependency state."""
    return {"status": "running"}


@router.get("/ready")
def ready(request: Request, response: Response) -> dict[str, str]:
    """Reports ready only once required configuration and dependencies are usable."""
    if not getattr(request.app.state, "ready", False):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "not ready"}
    return {"status": "ready"}
