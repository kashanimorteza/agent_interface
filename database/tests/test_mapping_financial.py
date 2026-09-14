"""Tests for the Financial Reference storage mappings (tasks P2-G4-T1..T3)."""

from __future__ import annotations

import model
import pytest

from database.exceptions import ConstraintViolation


def test_currency_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.Currency(user_id=user.id, code="USD"))
    fetched = db.get(model.Currency, created.id)
    assert fetched is not None
    assert fetched.user_id == user.id
    assert fetched.code == "USD"

    with pytest.raises(ConstraintViolation):
        db.create(model.Currency(user_id=user.id, code="USD"))


def test_broker_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.Broker(name="FxPro", user_id=user.id))
    fetched = db.get(model.Broker, created.id)
    assert fetched is not None
    assert fetched.name == "FxPro"

    with pytest.raises(ConstraintViolation):
        db.create(model.Broker(name="FxPro", user_id=user.id))


def test_asset_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    broker = db.create(model.Broker(name="FxPro", user_id=user.id))
    created = db.create(model.Asset(broker_id=broker.id, symbol="EUR/USD", category="Currency"))
    fetched = db.get(model.Asset, created.id)
    assert fetched is not None
    assert fetched.broker_id == broker.id
    assert fetched.symbol == "EUR/USD"

    with pytest.raises(ConstraintViolation):
        db.create(model.Asset(broker_id=broker.id, symbol="EUR/USD", category="Currency"))
