"""Verifies the Partial Rule Domain Definition (Task P1-G5-T4)."""

from __future__ import annotations

from decimal import Decimal

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import PartialRule

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "partial_group_id": True,
    "profit_percentage": True,
    "close_percentage": True,
    "status": False,
    "description": False,
}


def _make(**overrides):
    kwargs = {
        "id": 1,
        "name": "R1",
        "partial_group_id": 1,
        "profit_percentage": Decimal(50),
        "close_percentage": Decimal(25),
    }
    kwargs.update(overrides)
    return PartialRule(**kwargs)


def test_matches_target_definition() -> None:
    assert_exact_fields(PartialRule, EXPECTED_FIELDS)
    assert_credential_fields(PartialRule, ())
    assert_unique_constraints(
        PartialRule, (("name",), ("partial_group_id", "profit_percentage"))
    )


def test_defaults() -> None:
    rule = _make()
    assert rule.status is True
    assert rule.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        PartialRule(id=1, name="R1", partial_group_id=1)  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    rule = _make()
    assert PartialRule.model_validate_json(rule.model_dump_json()) == rule
    assert set(EXPECTED_FIELDS) <= set(PartialRule.model_json_schema()["properties"])
