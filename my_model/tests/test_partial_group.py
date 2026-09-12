from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.partial_group import PartialGroup


def test_valid_construction_succeeds() -> None:
    instance = PartialGroup(user_id=1, name="Default")
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        PartialGroup(name="Default")  # pyright: ignore[reportCallIssue] - deliberately missing user_id


def test_uniqueness_rule_is_declared() -> None:
    assert PartialGroup.UNIQUE_TOGETHER == (("user_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    assert PartialGroup.INITIAL_DATA == ({"user_id": 1, "name": "Default"},)
    PartialGroup.model_validate(PartialGroup.INITIAL_DATA[0])
