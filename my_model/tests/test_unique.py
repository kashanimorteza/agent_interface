"""Pure uniqueness-comparison helper: no I/O, deterministic."""

from __future__ import annotations

from my_model._unique import find_colliding_record, shares_unique_key
from my_model.broker import Broker


def test_shares_unique_key_true_for_matching_fields() -> None:
    a = Broker(name="FxPro", user_id=1)
    b = Broker(name="FxPro", user_id=1)
    assert shares_unique_key(a, b, ("user_id", "name")) is True


def test_shares_unique_key_false_for_differing_fields() -> None:
    a = Broker(name="FxPro", user_id=1)
    b = Broker(name="OtherBroker", user_id=1)
    assert shares_unique_key(a, b, ("user_id", "name")) is False


def test_find_colliding_record_returns_the_match() -> None:
    a = Broker(name="FxPro", user_id=1)
    b = Broker(name="FxPro", user_id=1)
    c = Broker(name="Different", user_id=1)
    assert find_colliding_record(a, [c, b], ("user_id", "name")) is b


def test_find_colliding_record_returns_none_without_a_match() -> None:
    a = Broker(name="FxPro", user_id=1)
    c = Broker(name="Different", user_id=1)
    assert find_colliding_record(a, [c], ("user_id", "name")) is None
