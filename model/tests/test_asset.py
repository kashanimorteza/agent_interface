"""Verifies the Asset Domain Definition (Task P1-G3-T3)."""

from __future__ import annotations

import pytest
from conftest import (
    assert_credential_fields,
    assert_exact_fields,
    assert_unique_constraints,
)
from pydantic import ValidationError

from model import Asset

EXPECTED_FIELDS = {
    "id": True,
    "broker_id": True,
    "symbol": True,
    "category": True,
    "point_size": False,
    "digits": False,
    "status": False,
    "description": False,
}


def test_matches_target_definition() -> None:
    assert_exact_fields(Asset, EXPECTED_FIELDS)
    assert_credential_fields(Asset, ())
    assert_unique_constraints(Asset, (("broker_id", "symbol"),))


def test_defaults() -> None:
    asset = Asset(id=1, broker_id=1, symbol="EUR/USD", category="Currency")
    assert asset.point_size == 0.0
    assert asset.digits == 0
    assert asset.status is True


def test_required_fields_enforced() -> None:
    with pytest.raises(ValidationError):
        Asset(id=1, broker_id=1, symbol="EUR/USD")  # pyright: ignore[reportCallIssue]


def test_serialization_and_schema() -> None:
    asset = Asset(
        id=1,
        broker_id=1,
        symbol="XAU/USD",
        category="Commodity",
        point_size=0.01,
        digits=2,
    )
    assert Asset.model_validate_json(asset.model_dump_json()) == asset
    assert set(EXPECTED_FIELDS) <= set(Asset.model_json_schema()["properties"])
