"""Tests for the Partial Group Domain Definition (task P1-G5-T3)."""

from __future__ import annotations

from model import PartialGroup


def _make() -> PartialGroup:
    return PartialGroup(user_id=1, name="Default")


def test_exact_field_set() -> None:
    assert set(PartialGroup.model_fields) == {"id", "user_id", "name", "is_active", "description"}


def test_uniqueness_on_user_and_name() -> None:
    assert PartialGroup.UNIQUE_CONSTRAINTS == (("user_id", "name"),)


def test_defaults() -> None:
    group = _make()
    assert group.is_active is True


def test_json_round_trip_and_schema() -> None:
    group = _make()
    restored = PartialGroup.model_validate_json(group.model_dump_json())
    assert restored == group
    assert PartialGroup.model_json_schema()["properties"]
