"""Verification for the Trailing Group Domain Definition (Task P1-trailing-group)."""

from __future__ import annotations

from conftest import (
    assert_public_interface,
    assert_rejects_missing_required,
    assert_rejects_null_for_non_nullable,
    assert_rejects_unknown_field,
    assert_rejects_wrong_type,
    assert_serialization_roundtrip,
    assert_valid_construction,
)

import model as model_module
from model import TrailingGroup

REQUIRED = ["user_id", "name"]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {"id": 1, "user_id": 1, "name": "Default"}


def test_public_interface():
    assert_public_interface(model_module, "TrailingGroup", TrailingGroup)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(TrailingGroup, _valid())
    assert instance.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(TrailingGroup, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(TrailingGroup, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(TrailingGroup, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(TrailingGroup, _valid(), "user_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(TrailingGroup(**_valid()))
