from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model.position import Position


def _valid() -> dict[str, object]:
    return {
        "user_id": 1,
        "name": "Pos-1",
        "trading_platform_id": 1,
        "broker_id": 1,
        "account_id": 1,
        "trailing_group_id": 1,
        "partial_group_id": 1,
        "action_group_id": 1,
        "action_id": 1,
        "date": datetime.now(UTC),
        "volume": Decimal(1),
        "order_type": "market",
        "base_tp": Decimal(1),
        "base_sl": Decimal(1),
        "real_tp": Decimal(1),
        "real_sl": Decimal(1),
    }


def test_valid_construction_succeeds() -> None:
    instance = Position.model_validate(_valid())
    assert instance.is_executed is False
    assert instance.profit == Decimal(0)


def test_missing_required_reference_is_rejected() -> None:
    data = _valid()
    del data["action_id"]
    with pytest.raises(ValidationError):
        Position.model_validate(data)


def test_naive_datetime_is_rejected() -> None:
    data = _valid()
    data["date"] = datetime.now()  # noqa: DTZ005 - deliberately naive, to prove it is rejected
    with pytest.raises(ValidationError):
        Position.model_validate(data)


def test_uniqueness_rule_is_declared() -> None:
    assert Position.UNIQUE_TOGETHER == (("name",),)
