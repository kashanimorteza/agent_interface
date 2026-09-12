from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model.action import Action


def _valid() -> dict[str, object]:
    return {
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


def test_valid_construction_succeeds() -> None:
    instance = Action.model_validate(_valid())
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    data = _valid()
    del data["stop_loss"]
    with pytest.raises(ValidationError):
        Action.model_validate(data)


def test_uniqueness_rule_is_declared() -> None:
    assert Action.UNIQUE_TOGETHER == (("action_group_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    record = Action.INITIAL_DATA[0]
    assert record["name"] == "Default"
    Action.model_validate(record)
