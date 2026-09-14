"""Verifies the Action Domain Definition (Task P1-G6-T2)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Action

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "action_group_id": True,
    "asset_id": True,
    "account_id": True,
    "partial_group_id": True,
    "trailing_group_id": True,
    "risk_by_reward": True,
    "take_profit": True,
    "stop_loss": True,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": Decimal(1),
        "take_profit": Decimal(1),
        "stop_loss": Decimal(1),
    }
    kwargs.update(overrides)
    return Action(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(Action, EXPECTED_FIELDS)
    assert_credential_fields(Action, ())
    assert_unique_constraints(Action, (("action_group_id", "name"),))


def test_defaults() -> None:
    action = _make()
    assert action.status is True
    assert action.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Action(id=1, name="Default", action_group_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    action = _make(risk_by_reward=Decimal("2.5"))
    assert Action.model_validate_json(action.model_dump_json()) == action
    assert set(EXPECTED_FIELDS) <= set(Action.model_json_schema()["properties"])
