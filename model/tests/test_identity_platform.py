"""Tests for User, Trading Platform, Instance, Currency, and Broker."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from model.broker import Broker
from model.currency import Currency
from model.foundation import ForeignKey, persistence_contract
from model.instance import Instance
from model.trading_platform import TradingPlatform
from model.user import User


def test_user_required_unique_and_defaults() -> None:
    user = User(name="Admin", username="admin", password="pw", api_key="key")
    assert user.id is None
    assert user.is_active is True
    assert user.description is None

    with pytest.raises(ValidationError):
        User(username="admin", password="pw", api_key="key")  # type: ignore[call-arg]

    contract = persistence_contract(User)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["name"].unique is True
    assert by_name["username"].unique is True
    assert by_name["password"].credential == "hash"
    assert by_name["api_key"].credential == "hash"
    assert by_name["id"].primary_key is True
    assert by_name["id"].auto_increment is True


def test_trading_platform_fields_and_uniqueness() -> None:
    platform = TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    assert platform.is_active is True

    contract = persistence_contract(TradingPlatform)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["name"].unique is True

    with pytest.raises(ValidationError):
        TradingPlatform(code="metatrader_5")  # type: ignore[call-arg]


def test_instance_relationships_credentials_and_composite_uniqueness() -> None:
    instance = Instance(
        user_id=1,
        trading_platform_id=1,
        name="MetaTrader",
        ip="127.0.0.1",
        username="test",
        password="secret",
        api_key="key",
    )
    assert instance.is_active is True

    contract = persistence_contract(Instance)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["user_id"].foreign_key == ForeignKey("User", "id")
    assert by_name["trading_platform_id"].foreign_key == ForeignKey("TradingPlatform", "id")
    assert by_name["password"].credential == "encrypted"
    assert by_name["api_key"].credential == "encrypted"
    assert contract.unique_sets == (("user_id", "name"),)

    with pytest.raises(ValidationError):
        Instance(trading_platform_id=1, name="x")  # type: ignore[call-arg]


def test_currency_code_length_and_defaults() -> None:
    currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
    assert currency.decimal_digits == 2

    with pytest.raises(ValidationError):
        Currency(user_id=1, code="US")

    with pytest.raises(ValidationError):
        Currency(user_id=1, code="USDX")

    contract = persistence_contract(Currency)
    assert contract.unique_sets == (("user_id", "code"),)


def test_broker_relationship_and_uniqueness() -> None:
    broker = Broker(name="FxPro", user_id=1)
    assert broker.is_active is True

    contract = persistence_contract(Broker)
    by_name = {f.name: f.meta for f in contract.fields}
    assert by_name["user_id"].foreign_key == ForeignKey("User", "id")
    assert contract.unique_sets == (("user_id", "name"),)


def test_precision_and_time_conventions() -> None:
    assert isinstance(Decimal("1.5"), Decimal)
    assert datetime.now(UTC).tzinfo is not None
