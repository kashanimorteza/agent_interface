"""Verifies P1T4: the Instance Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Instance

VALID = {
    "id": 1,
    "user_id": 1,
    "trading_platform_id": 1,
    "name": "MetaTrader",
    "ip": "127.0.0.1",
    "username": "test",
    "password": "secret",
    "api_key": "key",
}


@pytest.mark.parametrize("omit", ["user_id", "trading_platform_id", "name"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        Instance(**payload)


def test_valid_instance_round_trips_preserving_references() -> None:
    instance = Instance(**VALID)
    restored = Instance(**instance.model_dump())
    assert restored == instance
    assert restored.user_id == 1
    assert restored.trading_platform_id == 1


def test_published_metadata_declares_composite_unique_and_encrypted_credentials() -> (
    None
):
    meta = Instance.persistence_metadata()
    assert meta["unique_sets"] == [["user_id", "name"]]
    assert meta["fields"]["password"]["credential"] == "encrypted"
    assert meta["fields"]["api_key"]["credential"] == "encrypted"
    assert meta["fields"]["user_id"]["foreign_key"] == "user.id"
    assert meta["fields"]["trading_platform_id"]["foreign_key"] == "trading_platform.id"
