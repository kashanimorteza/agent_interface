"""Tests for the Position Domain Definition (task P1-G6-T3)."""

from __future__ import annotations

import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from model import Position


def _make() -> Position:
    return Position(
        user_id=1,
        name="Pos-1",
        trading_platform_id=1,
        broker_id=1,
        account_id=1,
        trailing_group_id=1,
        partial_group_id=1,
        action_group_id=1,
        action_id=1,
        date=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )


def test_exact_field_set() -> None:
    assert set(Position.model_fields) == {
        "id",
        "user_id",
        "name",
        "trading_platform_id",
        "broker_id",
        "account_id",
        "trailing_group_id",
        "partial_group_id",
        "action_group_id",
        "action_id",
        "date",
        "volume",
        "profit",
        "is_executed",
        "order_type",
        "base_tp",
        "base_sl",
        "real_tp",
        "real_sl",
        "is_active",
        "description",
    }


def test_uniqueness_on_name() -> None:
    assert Position.UNIQUE_CONSTRAINTS == (("name",),)


def test_naive_datetime_rejected() -> None:
    with pytest.raises(ValidationError):
        Position(
            user_id=1,
            name="Pos-2",
            trading_platform_id=1,
            broker_id=1,
            account_id=1,
            trailing_group_id=1,
            partial_group_id=1,
            action_group_id=1,
            action_id=1,
            date=datetime.datetime(2026, 1, 1),
            volume=Decimal("1"),
            order_type="market",
            base_tp=Decimal("1"),
            base_sl=Decimal("1"),
            real_tp=Decimal("1"),
            real_sl=Decimal("1"),
        )


def test_defaults() -> None:
    position = _make()
    assert position.profit == 0
    assert position.is_executed is False
    assert position.is_active is True


def test_json_round_trip_and_schema() -> None:
    position = _make()
    restored = Position.model_validate_json(position.model_dump_json())
    assert restored == position
    assert Position.model_json_schema()["properties"]
