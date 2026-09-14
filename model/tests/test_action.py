"""Verification for the Action Domain Definition (Task P1-action)."""

from __future__ import annotations

import decimal

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
from model import Action

REQUIRED = [
    "name",
    "action_group_id",
    "asset_id",
    "account_id",
    "partial_group_id",
    "trailing_group_id",
    "risk_by_reward",
    "take_profit",
    "stop_loss",
]
NON_NULLABLE = ["id", *REQUIRED, "is_active"]


def _valid() -> dict:
    return {
        "id": 1,
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": decimal.Decimal(1),
        "take_profit": decimal.Decimal(1),
        "stop_loss": decimal.Decimal(1),
    }


def test_public_interface():
    assert_public_interface(model_module, "Action", Action)


def test_valid_construction_and_defaults():
    instance = assert_valid_construction(Action, _valid())
    assert instance.is_active is True


def test_rejects_unknown_field():
    assert_rejects_unknown_field(Action, _valid())


def test_rejects_missing_required_fields():
    assert_rejects_missing_required(Action, _valid(), REQUIRED)


def test_rejects_null_for_non_nullable_fields():
    assert_rejects_null_for_non_nullable(Action, _valid(), NON_NULLABLE)


def test_rejects_wrong_type():
    assert_rejects_wrong_type(Action, _valid(), "asset_id")


def test_serialization_roundtrip():
    assert_serialization_roundtrip(Action(**_valid()))
