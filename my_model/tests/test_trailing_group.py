from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.trailing_group import TrailingGroup


def test_valid_construction_succeeds() -> None:
    instance = TrailingGroup(user_id=1, name="Default")
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TrailingGroup(name="Default")  # pyright: ignore[reportCallIssue] - deliberately missing user_id


def test_uniqueness_rule_is_declared() -> None:
    assert TrailingGroup.UNIQUE_TOGETHER == (("user_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    assert TrailingGroup.INITIAL_DATA == ({"user_id": 1, "name": "Default"},)
    TrailingGroup.model_validate(TrailingGroup.INITIAL_DATA[0])
