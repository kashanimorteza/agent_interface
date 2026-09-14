"""Tests for the shared Model Foundation (task P1-G1-T1)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import Broker, TradingPlatform, User


def _make_user() -> User:
    return User(name="Ada", username="ada", password="pw", api_key="key")


def _make_broker() -> Broker:
    return Broker(name="FxPro", user_id=1)


def _make_trading_platform() -> TradingPlatform:
    return TradingPlatform(name="MetaTrader 5", code="metatrader_5")


@pytest.mark.parametrize(
    ("factory_kwargs", "cls"),
    [
        ({"name": "Ada", "username": "ada", "password": "pw", "api_key": "key"}, User),
        ({"name": "FxPro", "user_id": 1}, Broker),
        ({"name": "MetaTrader 5", "code": "metatrader_5"}, TradingPlatform),
    ],
)
def test_unknown_field_rejected_consistently(factory_kwargs: dict, cls: type) -> None:
    with pytest.raises(ValidationError):
        cls(**factory_kwargs, unexpected_field="value")


@pytest.mark.parametrize("factory", [_make_user, _make_broker, _make_trading_platform])
def test_assignment_is_validated_consistently(factory) -> None:
    instance = factory()
    with pytest.raises(ValidationError):
        instance.name = 12345  # type: ignore[assignment]


def test_foundation_configuration_equal_across_domain_definitions() -> None:
    assert User.model_config == Broker.model_config == TradingPlatform.model_config
