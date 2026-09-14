"""Tests for the Identity and Connectivity storage mappings (tasks P2-G3-T1..T3)."""

from __future__ import annotations

import model
import pytest

from database.exceptions import ConstraintViolation


def test_user_mapping_preserves_fields_and_uniqueness_and_protects_credentials(db) -> None:
    created = db.create(model.User(name="Ada", username="ada", password="secret", api_key="key1"))
    assert created.id is not None
    fetched = db.get(model.User, created.id)
    assert fetched is not None
    assert fetched.name == "Ada"
    assert fetched.username == "ada"
    assert fetched.is_active is True
    # Credentials are never returned as plaintext through the generic interface.
    assert fetched.password != "secret"
    assert fetched.api_key != "key1"

    with pytest.raises(ConstraintViolation):
        db.create(model.User(name="Ada", username="ada2", password="x", api_key="y"))


def test_trading_platform_mapping_preserves_fields(db) -> None:
    created = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    fetched = db.get(model.TradingPlatform, created.id)
    assert fetched is not None
    assert fetched.name == "MetaTrader 5"
    assert fetched.code == "metatrader_5"


def test_instance_mapping_preserves_fields_relationships_uniqueness_and_credentials(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    platform = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))

    created = db.create(
        model.Instance(
            user_id=user.id,
            name="MetaTrader",
            trading_platform_id=platform.id,
            ip="127.0.0.1",
            username="test",
            password="secret",
            api_key="key123",
        )
    )
    fetched = db.get(model.Instance, created.id)
    assert fetched is not None
    assert fetched.user_id == user.id
    assert fetched.trading_platform_id == platform.id
    assert fetched.ip == "127.0.0.1"
    assert fetched.password != "secret"
    assert fetched.api_key != "key123"

    with pytest.raises(ConstraintViolation):
        db.create(
            model.Instance(user_id=user.id, name="MetaTrader", trading_platform_id=platform.id)
        )
