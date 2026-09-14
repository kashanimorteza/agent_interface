"""Verifies the Partial Group Domain Definition (Task P1-G5-T3)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import PartialGroup

EXPECTED_FIELDS = {
    "id": True,
    "user_id": True,
    "name": True,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(PartialGroup, EXPECTED_FIELDS)
    assert_credential_fields(PartialGroup, ())
    assert_unique_constraints(PartialGroup, (("user_id", "name"),))


def test_defaults() -> None:
    group = PartialGroup(id=1, user_id=1, name="Default")
    assert group.status is True
    assert group.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        PartialGroup(id=1, user_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    group = PartialGroup(id=1, user_id=1, name="Default")
    assert PartialGroup.model_validate_json(group.model_dump_json()) == group
    assert set(EXPECTED_FIELDS) <= set(PartialGroup.model_json_schema()["properties"])
