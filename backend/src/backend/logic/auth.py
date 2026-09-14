"""Authentication (task P3-G9-T1) and Authorization (task P3-G9-T2)."""

from __future__ import annotations

from ..database_interface import DatabaseInterface
from ..model_interface import User
from ..request_context import RequestContext
from .outcomes import Unauthenticated, Unauthorized


def authenticate(db: DatabaseInterface, api_key: str | None, *, request_id: str) -> RequestContext:
    """Establish the requester's identity from a submitted API key credential.

    Raises Unauthenticated when the credential is missing or does not match any active
    User. Never includes the submitted or stored credential value in the raised outcome.
    """
    if not api_key:
        raise Unauthenticated("A valid API key is required.")
    user_id = db.verify_credential(User, "api_key", api_key)
    if user_id is None:
        raise Unauthenticated("The submitted API key is not valid.")
    return RequestContext(request_id=request_id, user_id=user_id)


def authorize(context: RequestContext, *, operation: str) -> None:
    """Decide whether the established identity is authorized for `operation`.

    Consequential decision: the Target defines no differentiated permission model for
    this phase, so any authenticated identity is authorized for every operation Backend
    exposes. The decision is still made explicitly here, in Logic, rather than skipped
    or inferred from transport validity.
    """
    if not context.is_authenticated:
        raise Unauthorized(f"Authentication is required for {operation!r}.")
