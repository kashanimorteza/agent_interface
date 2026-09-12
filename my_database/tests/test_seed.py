from __future__ import annotations

from my_model.currency import Currency
from my_model.trading_platform import TradingPlatform
from my_model.user import User

from my_database import interface, seed


def test_seed_all_inserts_every_declared_initial_record():
    inserted = seed.seed_all()
    assert inserted > 0

    users = interface.list_(User)
    assert len(users) == 1
    assert users[0].name == "Admin"
    assert (
        users[0].password != "GENERATE_SECURELY"
    )  # resolved to a real generated value

    platforms = interface.list_(TradingPlatform)
    assert {p.code for p in platforms} == {"metatrader_5", "binance"}

    currencies = interface.list_(Currency)
    assert len(currencies) == 8


def test_seed_all_is_idempotent():
    first = seed.seed_all()
    second = seed.seed_all()
    assert first > 0
    assert second == 0
    # No duplicate records were created.
    assert len(interface.list_(User)) == 1
    assert len(interface.list_(TradingPlatform)) == 2
