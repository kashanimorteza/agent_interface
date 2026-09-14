"""Tests for the Account Group Domain Definition (task P1-G4-T1)."""

from __future__ import annotations

from model import AccountGroup


def _make() -> AccountGroup:
    return AccountGroup(user_id=1, name="Default")


def test_exact_field_set() -> None:
    assert set(AccountGroup.model_fields) == {"id", "user_id", "name", "is_active", "description"}


def test_uniqueness_on_user_and_name() -> None:
    assert AccountGroup.UNIQUE_CONSTRAINTS == (("user_id", "name"),)


def test_defaults() -> None:
    group = _make()
    assert group.is_active is True
    assert group.description is None


def test_json_round_trip_and_schema() -> None:
    group = _make()
    restored = AccountGroup.model_validate_json(group.model_dump_json())
    assert restored == group
    assert AccountGroup.model_json_schema()["properties"]
