"""Tests for the Action Group Domain Definition (task P1-G6-T1)."""

from __future__ import annotations

from model import ActionGroup


def _make() -> ActionGroup:
    return ActionGroup(user_id=1, name="Default")


def test_exact_field_set() -> None:
    assert set(ActionGroup.model_fields) == {"id", "user_id", "name", "is_active", "description"}


def test_uniqueness_on_user_and_name() -> None:
    assert ActionGroup.UNIQUE_CONSTRAINTS == (("user_id", "name"),)


def test_defaults() -> None:
    group = _make()
    assert group.is_active is True


def test_json_round_trip_and_schema() -> None:
    group = _make()
    restored = ActionGroup.model_validate_json(group.model_dump_json())
    assert restored == group
    assert ActionGroup.model_json_schema()["properties"]
