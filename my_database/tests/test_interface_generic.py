"""The same generic operations proven against two distinct, unrelated entities."""

from __future__ import annotations

import pytest
from my_model.broker import Broker
from my_model.trading_platform import TradingPlatform
from my_model.user import User

from my_database import interface


def _make_broker() -> Broker:
    user = interface.add(User(name="Ada", username="ada", password="x", api_key="y"))
    assert user.id is not None
    return Broker(name="FxPro", user_id=user.id)


@pytest.mark.parametrize(
    ("model_cls", "make"),
    [
        (Broker, _make_broker),
        (
            TradingPlatform,
            lambda: TradingPlatform(name="MetaTrader 5", code="metatrader_5"),
        ),
    ],
)
def test_add_get_list_update_delete_round_trip(model_cls, make):
    created = interface.add(make())
    assert created.id is not None

    fetched = interface.get(model_cls, created.id)
    assert fetched is not None
    assert fetched.id == created.id

    all_records = interface.list_(model_cls)
    assert any(r.id == created.id for r in all_records)

    updated = interface.update(model_cls, created.id, description="updated")
    assert updated.description == "updated"
    # unspecified fields are preserved (partial update)
    assert updated.name == created.name

    assert interface.delete(model_cls, created.id) is True
    assert interface.get(model_cls, created.id) is None
    assert interface.delete(model_cls, created.id) is False  # already gone


def test_get_missing_record_returns_none():
    assert interface.get(Broker, 999) is None


def test_update_missing_record_raises_not_found():
    with pytest.raises(interface.NotFoundError):
        interface.update(Broker, 999, description="x")


def test_list_supports_filters_ordering_and_pagination():
    for i in range(5):
        interface.add(TradingPlatform(name=f"Platform {i}", code=f"code_{i}"))

    filtered = interface.list_(TradingPlatform, code="code_2")
    assert len(filtered) == 1
    assert filtered[0].code == "code_2"

    paged = interface.list_(TradingPlatform, order_by="id", limit=2, offset=1)
    assert len(paged) == 2

    all_records = interface.list_(TradingPlatform, order_by="id")
    ids: list[int] = []
    for r in all_records:
        assert r.id is not None
        ids.append(r.id)
    assert ids == sorted(ids)
