"""Tests for the Transaction boundary (task P2-G9-T2)."""

from __future__ import annotations

import model
import pytest
from sqlalchemy.exc import OperationalError

from database.exceptions import TransactionConflict
from database.observability import transaction_conflict


def test_grouped_operations_leave_no_partial_effect_when_the_unit_fails(db) -> None:
    with pytest.raises(RuntimeError):
        with db.transaction() as txn:
            db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
            raise RuntimeError("deliberate failure partway through the unit")

    assert db.list(model.TradingPlatform) == ()


def test_successful_grouped_unit_makes_every_operation_visible_together(db) -> None:
    with db.transaction() as txn:
        db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
        db.create(model.TradingPlatform(name="Binance", code="binance"), txn=txn)

    names = {platform.name for platform in db.list(model.TradingPlatform)}
    assert names == {"MetaTrader 5", "Binance"}


def test_standalone_write_is_unaffected_by_another_units_rollback(db) -> None:
    db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    with pytest.raises(RuntimeError):
        with db.transaction() as txn:
            db.create(model.TradingPlatform(name="Binance", code="binance"), txn=txn)
            raise RuntimeError("fail this unit only")

    names = {platform.name for platform in db.list(model.TradingPlatform)}
    assert names == {"MetaTrader 5"}


def test_transaction_boundary_translates_operational_error_into_conflict_with_signal(
    db, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level("INFO", logger="database.signals")
    with pytest.raises(TransactionConflict):
        with db.transaction() as txn:
            db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
            raise OperationalError("statement", {}, Exception("database is locked"))

    assert any("transaction_conflict" in record.message for record in caplog.records)
    for record in caplog.records:
        assert "secret" not in record.message.lower()
    # The unit that hit the conflict rolled back; nothing it did is visible.
    assert db.list(model.TradingPlatform) == ()


def test_transaction_conflict_signal_never_carries_a_secret_value(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level("INFO", logger="database.signals")
    transaction_conflict("general", "SQLITE_BUSY")
    assert any("transaction_conflict" in record.message for record in caplog.records)
    for record in caplog.records:
        assert "secret" not in record.message.lower()
