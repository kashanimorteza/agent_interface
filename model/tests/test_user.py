"""Verifies P1T2: the User Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import User

VALID = {
    "id": 1,
    "name": "Admin",
    "username": "admin",
    "password": "secret",
    "api_key": "key",
}


@pytest.mark.parametrize("omit", ["name", "username", "password", "api_key"])
def test_required_field_omission_is_rejected(omit: str) -> None:
    payload = {k: v for k, v in VALID.items() if k != omit}
    with pytest.raises(ValidationError):
        User(**payload)


def test_valid_user_round_trips_through_serialization() -> None:
    user = User(**VALID)
    dumped = user.model_dump()
    restored = User(**dumped)
    assert restored == user
    assert restored.is_active is True
    assert restored.description is None


def test_published_metadata_declares_unique_and_credential_fields() -> None:
    meta = User.persistence_metadata()
    assert meta["persistent"] is True
    assert meta["fields"]["name"]["unique"] is True
    assert meta["fields"]["username"]["unique"] is True
    assert meta["fields"]["password"]["credential"] == "hash"
    assert meta["fields"]["api_key"]["credential"] == "hash"
    assert meta["fields"]["id"]["primary_key"] is True
    assert meta["fields"]["id"]["auto_increment"] is True
