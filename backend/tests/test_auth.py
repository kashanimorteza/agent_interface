"""Tests for Authentication (task P3-G9-T1) and Authorization (task P3-G9-T2)."""

from __future__ import annotations

import pytest

from backend.database_interface import DatabaseInterface
from backend.logic.auth import authenticate, authorize
from backend.logic.outcomes import Unauthenticated, Unauthorized
from backend.logic.user import UserLogic
from backend.request_context import RequestContext


def _di(db) -> DatabaseInterface:
    return DatabaseInterface(db, timeout_seconds=5.0, max_retry_attempts=3)


def test_valid_credential_establishes_the_correct_requester_identity(db) -> None:
    di = _di(db)
    user = UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "secret-key"}
    )
    ctx = authenticate(di, "secret-key", request_id="req-1")
    assert ctx.user_id == user.id
    assert ctx.is_authenticated


def test_missing_credential_is_rejected_before_logic_runs(db) -> None:
    di = _di(db)
    with pytest.raises(Unauthenticated):
        authenticate(di, None, request_id="req-1")


def test_invalid_credential_is_rejected(db) -> None:
    di = _di(db)
    UserLogic(di).create(
        {"name": "Ada", "username": "ada", "password": "pw", "api_key": "secret-key"}
    )
    with pytest.raises(Unauthenticated):
        authenticate(di, "wrong-key", request_id="req-1")


def test_authentication_failure_never_carries_the_credential_value(db) -> None:
    di = _di(db)
    try:
        authenticate(di, "some-candidate-value", request_id="req-1")
    except Unauthenticated as exc:
        assert "some-candidate-value" not in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected Unauthenticated")


def test_authorize_requires_an_authenticated_context() -> None:
    with pytest.raises(Unauthorized):
        authorize(RequestContext(request_id="req-1", user_id=None), operation="create_User")


def test_authorize_permits_an_authenticated_context() -> None:
    authorize(RequestContext(request_id="req-1", user_id=1), operation="create_User")  # no raise
