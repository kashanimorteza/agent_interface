from __future__ import annotations

import pytest
from pydantic import ValidationError

from my_model.trading_platform import TradingPlatform


def test_valid_construction_succeeds() -> None:
    instance = TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    assert instance.status is True


def test_missing_required_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TradingPlatform(name="MetaTrader 5")  # pyright: ignore[reportCallIssue] - deliberately missing code


def test_declared_initial_records_are_present() -> None:
    assert TradingPlatform.INITIAL_DATA == (
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    )
    for record in TradingPlatform.INITIAL_DATA:
        TradingPlatform.model_validate(record)
