"""Verifies the Model Foundation's shared configuration and behavior (Task P1-G1-T1)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

import model

SAMPLES = [
    (
        model.User,
        {"id": 1, "name": "A", "username": "a", "password": "p", "api_key": "k"},
    ),
    (model.Broker, {"id": 1, "name": "FxPro", "user_id": 1}),
    (model.TradingPlatform, {"id": 1, "name": "Binance", "code": "binance"}),
]

DOMAIN_DEFINITIONS = [
    getattr(model, name)
    for name in model.__all__
    if isinstance(getattr(model, name), type)
    and issubclass(getattr(model, name), model.ModelBase)
]


@pytest.mark.parametrize("model_cls,kwargs", SAMPLES)
def test_unknown_field_rejected_consistently(model_cls, kwargs) -> None:
    with pytest.raises(ValidationError):
        model_cls(**kwargs, not_a_real_field="nope")


@pytest.mark.parametrize("model_cls,kwargs", SAMPLES)
def test_assignment_validated_consistently(model_cls, kwargs) -> None:
    instance = model_cls(**kwargs)
    with pytest.raises(ValidationError):
        instance.id = "not-an-int"


def test_shared_behavior_comes_only_from_the_foundation() -> None:
    """Every Domain Definition's effective configuration is the Foundation's, not its own variant."""

    for cls in DOMAIN_DEFINITIONS:
        if cls is model.ModelBase:
            continue
        assert cls.model_config == model.ModelBase.model_config, (
            f"{cls.__name__} carries configuration that differs from the Model Foundation's"
        )
