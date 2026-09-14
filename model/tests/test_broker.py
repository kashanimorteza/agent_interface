"""Tests for the Broker Domain Definition (task P1-G3-T2)."""

from __future__ import annotations

from model import Broker


def _make() -> Broker:
    return Broker(name="FxPro", user_id=1)


def test_exact_field_set() -> None:
    assert set(Broker.model_fields) == {"id", "name", "user_id", "is_active", "description"}


def test_uniqueness_on_user_and_name() -> None:
    assert Broker.UNIQUE_CONSTRAINTS == (("user_id", "name"),)


def test_defaults() -> None:
    broker = _make()
    assert broker.is_active is True
    assert broker.description is None


def test_json_round_trip_and_schema() -> None:
    broker = _make()
    restored = Broker.model_validate_json(broker.model_dump_json())
    assert restored == broker
    assert Broker.model_json_schema()["properties"]
