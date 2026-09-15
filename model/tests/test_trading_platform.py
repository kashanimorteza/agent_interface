"""Verifies P1T3: the Trading Platform Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import TradingPlatform

VALID = {"id": 1, "name": "MetaTrader 5", "code": "metatrader_5"}


@pytest.mark.parametrize("omit", ["name", "code"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        TradingPlatform(**payload)


def test_valid_trading_platform_round_trips_through_serialization() -> None:
    platform = TradingPlatform(**VALID)
    restored = TradingPlatform(**platform.model_dump())
    assert restored == platform


def test_published_metadata_declares_name_as_unique() -> None:
    meta = TradingPlatform.persistence_metadata()
    assert meta["persistent"] is True
    assert meta["fields"]["name"]["unique"] is True
