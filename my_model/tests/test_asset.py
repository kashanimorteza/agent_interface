from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.asset import Asset


def test_valid_construction_succeeds() -> None:
    instance = Asset(broker_id=1, symbol="EUR/USD", category="Currency")
    assert instance.point_size == 0.0
    assert instance.digits == 0


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Asset(broker_id=1, symbol="EUR/USD")  # pyright: ignore[reportCallIssue] - deliberately missing category


def test_uniqueness_rule_is_declared() -> None:
    assert Asset.UNIQUE_TOGETHER == (("broker_id", "symbol"),)


def test_declared_initial_records_are_present() -> None:
    assert len(Asset.INITIAL_DATA) == 4
    symbols = {record["symbol"] for record in Asset.INITIAL_DATA}
    assert symbols == {"EUR/USD", "EUR/GBP", "XAU/USD", "USOil"}
    for record in Asset.INITIAL_DATA:
        Asset.model_validate(record)
