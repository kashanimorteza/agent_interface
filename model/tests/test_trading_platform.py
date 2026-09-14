"""Verifies the Trading Platform Domain Definition (Task P1-G2-T2)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import TradingPlatform

EXPECTED_FIELDS = {
    "id": True,
    "name": True,
    "code": True,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(TradingPlatform, EXPECTED_FIELDS)
    assert_credential_fields(TradingPlatform, ())
    assert_unique_constraints(TradingPlatform, ())


def test_defaults() -> None:
    platform = TradingPlatform(id=1, name="MetaTrader 5", code="metatrader_5")
    assert platform.status is True
    assert platform.description is None


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        TradingPlatform(id=1, name="Binance")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    platform = TradingPlatform(id=2, name="Binance", code="binance")
    assert TradingPlatform.model_validate_json(platform.model_dump_json()) == platform
    assert set(EXPECTED_FIELDS) <= set(
        TradingPlatform.model_json_schema()["properties"]
    )
