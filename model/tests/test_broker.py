"""Verifies the Broker Domain Definition (Task P1-G3-T2)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Broker

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "user_id": True,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(Broker, EXPECTED_FIELDS)
    assert_credential_fields(Broker, ())
    assert_unique_constraints(Broker, (("user_id", "name"),))


def test_defaults() -> None:
    broker = Broker(id=1, name="FxPro", user_id=1)
    assert broker.status is True
    assert broker.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Broker(id=1, name="FxPro")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    broker = Broker(id=1, name="FxPro", user_id=1)
    assert Broker.model_validate_json(broker.model_dump_json()) == broker
    assert set(EXPECTED_FIELDS) <= set(Broker.model_json_schema()["properties"])
