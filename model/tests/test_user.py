"""Verifies the User Domain Definition (Task P1-G2-T1)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import User

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "username": True,
    "password": True,
    "api_key": True,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "name": "Admin",
        "username": "admin",
        "password": "secret",
        "api_key": "key",
    }
    kwargs.update(overrides)
    return User(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(User, EXPECTED_FIELDS)
    assert_credential_fields(User, ("password", "api_key"))
    assert_unique_constraints(User, (("name",),))


def test_defaults() -> None:
    user = _make()
    assert user.status is True
    assert user.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        User(id=1, name="Admin")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    user = _make()
    assert User.model_validate_json(user.model_dump_json()) == user
    assert set(EXPECTED_FIELDS) <= set(User.model_json_schema()["properties"])
