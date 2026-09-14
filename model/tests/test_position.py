"""Verifies the Position Domain Definition (Task P1-G6-T3)."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Position

EXPECTED_FIELDS = {
    "id": True,
    "user_id": True,
    "name": True,
    "trading_platform_id": True,
    "broker_id": True,
    "account_id": True,
    "trailing_group_id": True,
    "partial_group_id": True,
    "action_group_id": True,
    "action_id": True,
    "date": True,
    "volume": True,
    "profit": False,
    "is_executed": False,
    "order_type": True,
    "base_tp": True,
    "base_sl": True,
    "real_tp": True,
    "real_sl": True,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "user_id": 1,
        "name": "Pos-1",
        "trading_platform_id": 1,
        "broker_id": 1,
        "account_id": 1,
        "trailing_group_id": 1,
        "partial_group_id": 1,
        "action_group_id": 1,
        "action_id": 1,
        "date": datetime(2026, 1, 1, tzinfo=UTC),
        "volume": Decimal(1),
        "order_type": "market",
        "base_tp": Decimal(1),
        "base_sl": Decimal(1),
        "real_tp": Decimal(1),
        "real_sl": Decimal(1),
    }
    kwargs.update(overrides)
    return Position(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(Position, EXPECTED_FIELDS)
    assert_credential_fields(Position, ())
    assert_unique_constraints(Position, (("name",),))


def test_defaults() -> None:
    position = _make()
    assert position.profit == Decimal(0)
    assert position.is_executed is False
    assert position.status is True


def test_naive_datetime_rejected() -> None:
    with pytest.raises(ValidationError):
        _make(date=datetime(2026, 1, 1))  # noqa: DTZ001 - deliberately naive


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Position(id=1, user_id=1, name="Pos-1")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    position = _make()
    assert Position.model_validate_json(position.model_dump_json()) == position
    assert set(EXPECTED_FIELDS) <= set(Position.model_json_schema()["properties"])
