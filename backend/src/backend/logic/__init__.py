"""Backend's Logic: the Logic Foundation, Authentication/Authorization, and every Model
Logic unit, exposed through the Logic registry."""

from __future__ import annotations

from .auth import authenticate, authorize
from .foundation import ModelLogicBase
from .outcomes import (
    ApplicationOutcome,
    ConflictOutcome,
    NotFound,
    Unauthenticated,
    Unauthorized,
    ValidationFailed,
)
from .registry import LOGIC_REGISTRY

__all__ = [
    "LOGIC_REGISTRY",
    "ApplicationOutcome",
    "ConflictOutcome",
    "ModelLogicBase",
    "NotFound",
    "Unauthenticated",
    "Unauthorized",
    "ValidationFailed",
    "authenticate",
    "authorize",
]
