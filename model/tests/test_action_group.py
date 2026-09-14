"""Verifies the Action Group Domain Definition (Task P1-G6-T1)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import ActionGroup

EXPECTED_FIELDS = {
    "id": True,
    "user_id": True,
    "name": True,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(ActionGroup, EXPECTED_FIELDS)
    assert_credential_fields(ActionGroup, ())
    assert_unique_constraints(ActionGroup, (("user_id", "name"),))


def test_defaults() -> None:
    group = ActionGroup(id=1, user_id=1, name="Default")
    assert group.status is True
    assert group.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        ActionGroup(id=1, user_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    group = ActionGroup(id=1, user_id=1, name="Default")
    assert ActionGroup.model_validate_json(group.model_dump_json()) == group
    assert set(EXPECTED_FIELDS) <= set(ActionGroup.model_json_schema()["properties"])
