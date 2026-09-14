"""Tests for the generic Database Interface (task P2-G9-T1)."""

from __future__ import annotations

import model
import pytest

from database.exceptions import ConstraintViolation


def test_generic_interface_performs_all_operations_for_more_than_one_domain_definition(db) -> None:
    # TradingPlatform: create, read, read-by-id, list, update, delete.
    platform = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    assert db.get(model.TradingPlatform, platform.id) is not None
    assert platform in db.list(model.TradingPlatform)
    updated = db.update(platform.model_copy(update={"description": "primary"}))
    assert updated.description == "primary"
    db.delete(model.TradingPlatform, platform.id)
    assert db.get(model.TradingPlatform, platform.id) is None

    # Broker: the same generic operations, via the same interface, no dedicated entry point.
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    broker = db.create(model.Broker(name="FxPro", user_id=user.id))
    assert db.get(model.Broker, broker.id) is not None
    assert broker in db.list(model.Broker)


def test_activation_available_only_when_is_active_field_declared(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    deactivated = db.activate(model.User, user.id, enable=False)
    assert deactivated.is_active is False
    reactivated = db.activate(model.User, user.id, enable=True)
    assert reactivated.is_active is True

    # Every Domain Definition in this Target happens to declare is_active, so a synthetic
    # type without it proves the "unavailable where absent" branch is actually enforced.
    from model.foundation import ModelBase

    class NoActiveStateField(ModelBase):
        name: str

    with pytest.raises(ValueError, match="is_active"):
        db.activate(NoActiveStateField, 1, enable=False)


def test_operations_require_the_domain_definitions_public_type_not_a_name_string(db) -> None:
    with pytest.raises((KeyError, ValueError, AttributeError, TypeError)):
        db.get("User", 1)  # type: ignore[arg-type]


def test_constraint_violation_signals_and_never_bypasses_uniqueness(
    db, caplog: pytest.LogCaptureFixture
) -> None:
    db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    caplog.clear()
    caplog.set_level("INFO", logger="database.signals")
    with pytest.raises(ConstraintViolation):
        db.create(model.User(name="Ada", username="ada2", password="x", api_key="y"))
    assert any("constraint_violation" in record.message for record in caplog.records)


def test_credential_access_signal_on_read(db, caplog: pytest.LogCaptureFixture) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    caplog.clear()
    caplog.set_level("INFO", logger="database.signals")
    db.get(model.User, user.id)
    assert any("protected_data_access" in record.message for record in caplog.records)
    for record in caplog.records:
        assert "pw" not in record.message
