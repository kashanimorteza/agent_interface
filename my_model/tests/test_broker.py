from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.broker import Broker


def test_valid_construction_succeeds() -> None:
    instance = Broker(name="FxPro", user_id=1)
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Broker(name="FxPro")  # pyright: ignore[reportCallIssue] - deliberately missing user_id


def test_uniqueness_rule_is_declared() -> None:
    assert Broker.UNIQUE_TOGETHER == (("user_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    assert Broker.INITIAL_DATA == ({"name": "FxPro", "user_id": 1},)
    Broker.model_validate(Broker.INITIAL_DATA[0])
