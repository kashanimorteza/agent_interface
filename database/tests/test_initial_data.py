"""Verifies P2T9: importing Target-declared initial data, repeatably."""

from __future__ import annotations

from model import Account, Asset, Currency, TradingPlatform, User

from database import interface as db
from database.initial_data import INITIAL_RECORDS, import_initial_data


def test_import_creates_exactly_the_declared_records(fresh_db: None) -> None:
    refs = import_initial_data()
    assert len(refs) == len(INITIAL_RECORDS)

    assert len(db.list_(User)) == 1
    assert len(db.list_(TradingPlatform)) == 2
    assert len(db.list_(Currency)) == 8
    assert len(db.list_(Asset)) == 4
    assert len(db.list_(Account)) == 1


def test_import_relationships_are_correctly_resolved(fresh_db: None) -> None:
    import_initial_data()
    account = db.list_(Account)[0]
    currency = db.get_by_id(Currency, account.base_currency_id)
    assert currency.code == "USD"


def test_import_generates_and_protects_declared_credentials(fresh_db: None) -> None:
    import_initial_data()
    user = db.list_(User)[0]
    assert user.password != ""
    assert (
        "$" in user.password
    )  # hash treatment format, never the plaintext "Generate securely"


def test_import_is_repeatable_without_duplication(fresh_db: None) -> None:
    first = import_initial_data()
    second = import_initial_data()
    assert first == second
    assert len(db.list_(User)) == 1
    assert len(db.list_(TradingPlatform)) == 2
    assert len(db.list_(Account)) == 1
