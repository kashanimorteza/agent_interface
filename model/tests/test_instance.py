"""Verifies the Instance Domain Definition (Task P1-G2-T3)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Instance

EXPECTED_FIELDS = {
    "id": True,
    "user_id": True,
    "name": True,
    "trading_platform_id": True,
    "ip": False,
    "username": False,
    "password": False,
    "api_key": False,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {"id": 1, "user_id": 1, "name": "MetaTrader", "trading_platform_id": 1}
    kwargs.update(overrides)
    return Instance(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(Instance, EXPECTED_FIELDS)
    assert_credential_fields(Instance, ("password", "api_key"))
    assert_unique_constraints(Instance, (("user_id", "name"),))


def test_defaults() -> None:
    instance = _make()
    assert instance.status is True
    assert instance.ip is None
    assert instance.username is None
    assert instance.password is None
    assert instance.api_key is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Instance(id=1, user_id=1, name="MetaTrader")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    instance = _make(ip="127.0.0.1", username="test", password="secret", api_key="key")
    assert Instance.model_validate_json(instance.model_dump_json()) == instance
    assert set(EXPECTED_FIELDS) <= set(Instance.model_json_schema()["properties"])
