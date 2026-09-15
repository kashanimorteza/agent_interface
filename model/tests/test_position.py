from datetime import UTC, datetime
from decimal import Decimal

import pytest
from conftest import (
    assert_rejects_unknown_field,
    assert_requires_field,
    assert_serializes_and_generates_schema,
)
from pydantic import ValidationError

from model import Position

VALID = {
    "user_id": 1,
    "name": "Pos-1",
    "trading_platform_id": 1,
    "broker_id": 1,
    "account_id": 1,
    "trailing_group_id": 1,
    "partial_group_id": 1,
    "action_group_id": 1,
    "action_id": 1,
    "date": datetime(2026, 9, 15, tzinfo=UTC),
    "volume": Decimal(1),
    "order_type": "market",
    "base_tp": Decimal(1),
    "base_sl": Decimal(1),
    "real_tp": Decimal(1),
    "real_sl": Decimal(1),
}


def test_valid_construction_applies_declared_defaults():
    position = Position.model_validate(VALID)
    assert position.profit == 0
    assert position.is_executed is False
    assert position.is_active is True


def test_date_must_be_timezone_aware():
    with pytest.raises(ValidationError):
        Position.model_validate({**VALID, "date": datetime(2026, 9, 15)})  # noqa: DTZ001


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Position, VALID)


def test_requires_declared_non_nullable_fields():
    for field in (
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
        "order_type",
        "base_tp",
        "base_sl",
        "real_tp",
        "real_sl",
    ):
        assert_requires_field(Position, VALID, field)


def test_publishes_relationships_and_uniqueness_metadata():
    contract = Position.persistence_contract()
    assert contract.fields["name"].unique is True
    references = {r.field: r.references for r in contract.relationships}
    assert references == {
        "user_id": "User",
        "trading_platform_id": "TradingPlatform",
        "broker_id": "Broker",
        "account_id": "Account",
        "trailing_group_id": "TrailingGroup",
        "partial_group_id": "PartialGroup",
        "action_group_id": "ActionGroup",
        "action_id": "Action",
    }
    assert contract.fields["profit"].default == Decimal(0)
    assert contract.fields["is_executed"].default is False


def test_serializes_and_generates_schema():
    assert_serializes_and_generates_schema(Position.model_validate(VALID))
