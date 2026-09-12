"""Every Model's Logic unit, the shared baseline, and application-context
validation of the resulting domain state (Task P3-T3).
"""

from __future__ import annotations

import my_model as m
import pytest

from backend import data_access
from backend.logic import REGISTRY


def test_every_persistent_model_has_its_own_logic_unit():
    persistent_models = [
        m.User,
        m.TradingPlatform,
        m.Instance,
        m.Currency,
        m.Broker,
        m.Asset,
        m.AccountGroup,
        m.Account,
        m.TrailingGroup,
        m.TrailingRule,
        m.PartialGroup,
        m.PartialRule,
        m.ActionGroup,
        m.Action,
        m.Position,
    ]
    for model_type in persistent_models:
        assert model_type in REGISTRY
        assert REGISTRY[model_type].model_type is model_type

    unit_classes = {type(logic) for logic in REGISTRY.values()}
    assert len(unit_classes) == len(persistent_models)  # each Model has its own class


def test_logic_create_get_list_update_delete():
    logic = REGISTRY[m.Broker]
    created = logic.create(name="LogicBrokerA", user_id=1)
    assert logic.get(created.id).name == "LogicBrokerA"
    assert any(b.id == created.id for b in logic.list(user_id=1))

    updated = logic.update(created.id, description="via logic")
    assert updated.description == "via logic"
    assert updated.name == "LogicBrokerA"

    logic.delete(created.id)
    with pytest.raises(data_access.NotFound):
        logic.get(created.id)


def test_partial_update_leaving_an_invalid_resulting_state_is_rejected():
    logic = REGISTRY[m.Broker]
    created = logic.create(name="LogicBrokerB", user_id=1)
    with pytest.raises(data_access.ValidationFailed):
        logic.update(created.id, name="")  # resulting state violates Broker's own rule


def test_status_available_for_a_model_that_declares_the_field():
    logic = REGISTRY[m.TradingPlatform]
    created = logic.create(name="LogicStatusPlatform", code="logic_status")
    disabled = logic.set_status(created.id, "disable")
    assert disabled.status is False


def test_status_rejected_for_a_model_without_the_field():
    from backend.logic import ModelLogic

    class NoStatusModel(m.BaseModel):
        id: int | None = None
        name: str

    class NoStatusLogic(ModelLogic[NoStatusModel]):
        model_type = NoStatusModel

    with pytest.raises(data_access.UnsupportedOperation):
        NoStatusLogic().set_status(1, "enable")
