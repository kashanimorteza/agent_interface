"""The generic Model-driven CRUD pipeline and status operation (Tasks P2-T5, P2-T6)."""

from __future__ import annotations

import my_model as m
import pytest

import my_database as db
from my_database.exceptions import (
    ConstraintViolation,
    NotFound,
    UnsupportedOperation,
    ValidationFailed,
)


def test_add_and_get_round_trip_for_multiple_distinct_models():
    broker = db.operations.add(m.Broker, instance="general", name="OpsBrokerA", user_id=1)
    currency = db.operations.add(m.Currency, instance="general", user_id=1, code="ABC")

    assert db.operations.get(m.Broker, broker.id, instance="general").name == "OpsBrokerA"
    assert db.operations.get(m.Currency, currency.id, instance="general").code == "ABC"


def test_add_populates_generated_id_and_redacts_credentials():
    user = db.operations.add(
        m.User,
        instance="general",
        name="OpsUser",
        username="opsuser",
        password="p4ss!",
        api_key="k3y!",
    )
    assert isinstance(user.id, int)
    assert user.password == "••••••••"
    assert user.api_key == "••••••••"


def test_get_raises_not_found_for_missing_identifier():
    with pytest.raises(NotFound):
        db.operations.get(m.Broker, 999_999, instance="general")


def test_list_filters_by_exact_criteria_and_orders_by_id():
    a = db.operations.add(m.AccountGroup, instance="general", user_id=1, name="ListGroupA")
    b = db.operations.add(m.AccountGroup, instance="general", user_id=1, name="ListGroupB")
    results = db.operations.list(m.AccountGroup, instance="general", user_id=1)
    ids = [r.id for r in results]
    assert a.id in ids and b.id in ids
    assert ids == sorted(ids)


def test_update_changes_only_supplied_fields():
    broker = db.operations.add(m.Broker, instance="general", name="UpdateBrokerA", user_id=1)
    updated = db.operations.update(
        m.Broker, broker.id, instance="general", description="new description"
    )
    assert updated.description == "new description"
    assert updated.name == "UpdateBrokerA"


def test_update_rejects_a_violated_model_rule():
    broker = db.operations.add(m.Broker, instance="general", name="UpdateBrokerB", user_id=1)
    with pytest.raises(ValidationFailed):
        db.operations.update(m.Broker, broker.id, instance="general", name="")


def test_delete_removes_an_unreferenced_record():
    broker = db.operations.add(m.Broker, instance="general", name="DeleteBrokerA", user_id=1)
    db.operations.delete(m.Broker, broker.id, instance="general")
    with pytest.raises(NotFound):
        db.operations.get(m.Broker, broker.id, instance="general")


def test_delete_rejects_a_referenced_record():
    seeded_broker = db.operations.list(m.Broker, instance="general", name="FxPro")[0]
    with pytest.raises(ConstraintViolation):
        db.operations.delete(m.Broker, seeded_broker.id, instance="general")


def test_add_rejects_an_unresolvable_foreign_key():
    with pytest.raises(ConstraintViolation):
        db.operations.add(m.Broker, instance="general", name="GhostBroker", user_id=999_999)


def test_add_rejects_a_duplicate_of_a_unique_field():
    with pytest.raises(ConstraintViolation):
        db.operations.add(
            m.User, instance="general", name="Admin", username="dupe", password="x", api_key="y"
        )


def test_add_rejects_invalid_payload_before_touching_storage():
    with pytest.raises(ValidationFailed):
        db.operations.add(
            m.User, instance="general", name="", username="x", password="y", api_key="z"
        )


def test_status_operation_enables_and_disables():
    platform = db.operations.add(
        m.TradingPlatform, instance="general", name="StatusPlatform", code="status_test"
    )
    disabled = db.operations.set_status(
        m.TradingPlatform, platform.id, "disable", instance="general"
    )
    assert disabled.status is False
    enabled = db.operations.set_status(m.TradingPlatform, platform.id, "enable", instance="general")
    assert enabled.status is True


def test_status_operation_rejected_for_a_model_without_status():
    class NoStatusModel(m.BaseModel):
        id: int | None = None
        name: str

    with pytest.raises(UnsupportedOperation):
        db.operations.set_status(NoStatusModel, 1, "enable", instance="general")
