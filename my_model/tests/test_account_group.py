from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.account_group import AccountGroup


def test_valid_construction_succeeds() -> None:
    instance = AccountGroup(user_id=1, name="Default")
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AccountGroup(name="Default")  # pyright: ignore[reportCallIssue] - deliberately missing user_id


def test_uniqueness_rule_is_declared() -> None:
    assert AccountGroup.UNIQUE_TOGETHER == (("user_id", "name"),)


def test_declared_initial_record_is_present() -> None:
    assert AccountGroup.INITIAL_DATA == ({"user_id": 1, "name": "Default"},)
    AccountGroup.model_validate(AccountGroup.INITIAL_DATA[0])
