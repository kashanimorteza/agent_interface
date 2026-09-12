"""Domain validation checks for every entity in the my_model package.

Covers valid construction, rejection of invalid states, boundary values,
defaults, omitted-versus-explicit-null semantics, declared relationships
(as typed identifier fields), and declared initial data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

import my_model as m


def test_user_valid_and_defaults() -> None:
    user = m.User(name="Ada", username="ada", password="secret", api_key="key")
    assert user.id is None
    assert user.status is True
    assert user.description is None


def test_user_rejects_blank_required_field() -> None:
    with pytest.raises(ValidationError):
        m.User(name="", username="ada", password="secret", api_key="key")


def test_user_rejects_unknown_field() -> None:
    with pytest.raises(ValidationError):
        m.User.model_validate(
            {
                "name": "Ada",
                "username": "ada",
                "password": "secret",
                "api_key": "key",
                "extra": "nope",
            }
        )


def test_user_initial_data_declares_admin() -> None:
    (record,) = m.User.initial_data
    assert record["username"] == "admin"
    assert record["password"] is m.GENERATE_SECURELY
    assert record["api_key"] is m.GENERATE_SECURELY


def test_user_credential_fields_declared() -> None:
    assert m.User.credential_fields == frozenset({"password", "api_key"})


def test_trading_platform_valid_and_initial_data() -> None:
    platform = m.TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    assert platform.status is True
    codes = {record["code"] for record in m.TradingPlatform.initial_data}
    assert codes == {"metatrader_5", "binance"}


def test_trading_platform_rejects_blank_code() -> None:
    with pytest.raises(ValidationError):
        m.TradingPlatform(name="MT5", code="")


def test_instance_valid_with_optional_connection_fields_omitted() -> None:
    instance = m.Instance(user_id=1, name="Primary", trading_platform_id=1)
    assert instance.ip is None
    assert instance.password is None


def test_instance_explicit_null_distinct_from_omission() -> None:
    omitted = m.Instance(user_id=1, name="Primary", trading_platform_id=1)
    explicit_null = m.Instance(user_id=1, name="Primary", trading_platform_id=1, ip=None)
    assert omitted.ip is None
    assert explicit_null.ip is None
    assert omitted.model_dump() == explicit_null.model_dump()


def test_instance_enforces_declared_platform_requirement() -> None:
    original = dict(m.Instance.platform_required_fields)
    try:
        m.Instance.platform_required_fields = {1: frozenset({"ip"})}
        with pytest.raises(ValidationError):
            m.Instance(user_id=1, name="Primary", trading_platform_id=1)
        m.Instance(user_id=1, name="Primary", trading_platform_id=1, ip="127.0.0.1")
    finally:
        m.Instance.platform_required_fields = original


def test_instance_credential_fields_declared() -> None:
    assert m.Instance.credential_fields == frozenset({"password", "api_key"})


def test_currency_valid_and_defaults() -> None:
    currency = m.Currency(user_id=1, code="USD")
    assert currency.decimal_digits == 2
    assert len(m.Currency.initial_data) == 8


def test_currency_rejects_wrong_length_code() -> None:
    with pytest.raises(ValidationError):
        m.Currency(user_id=1, code="US")


def test_currency_rejects_negative_decimal_digits() -> None:
    with pytest.raises(ValidationError):
        m.Currency(user_id=1, code="USD", decimal_digits=-1)


def test_broker_valid_and_initial_data() -> None:
    broker = m.Broker(name="FxPro", user_id=1)
    assert broker.status is True
    assert m.Broker.initial_data == ({"name": "FxPro", "user_id": 1},)


def test_asset_valid_and_boundary_zero_allowed() -> None:
    asset = m.Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0, digits=0)
    assert asset.point_size == 0.0


def test_asset_rejects_negative_point_size() -> None:
    with pytest.raises(ValidationError):
        m.Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=-0.01, digits=5)


def test_account_group_valid_and_initial_data() -> None:
    group = m.AccountGroup(user_id=1, name="Default")
    assert group.status is True
    assert m.AccountGroup.initial_data == ({"user_id": 1, "name": "Default"},)


def test_account_valid_and_defaults() -> None:
    account = m.Account(
        name="Acc-1",
        group_id=1,
        broker_id=1,
        instance_id=1,
        base_currency_id=1,
        username="test",
        password="secret",
        leverage=100,
        account_type="CFD",
    )
    assert account.balance == Decimal("0")
    assert account.status is True


def test_account_rejects_non_positive_leverage() -> None:
    with pytest.raises(ValidationError):
        m.Account(
            name="Acc-1",
            group_id=1,
            broker_id=1,
            instance_id=1,
            base_currency_id=1,
            username="test",
            password="secret",
            leverage=0,
            account_type="CFD",
        )


def test_account_credential_fields_declared() -> None:
    assert m.Account.credential_fields == frozenset({"password"})


def test_trailing_group_valid() -> None:
    group = m.TrailingGroup(user_id=1, name="Default")
    assert group.status is True


def test_trailing_rule_valid_and_optional_adjustments() -> None:
    rule = m.TrailingRule(name="Rule 1", trailing_group_id=1, trigger_percentage=Decimal("50"))
    assert rule.take_profit_adjustment is None
    assert rule.stop_loss_adjustment is None


def test_trailing_rule_rejects_negative_trigger_percentage() -> None:
    with pytest.raises(ValidationError):
        m.TrailingRule(name="Rule 1", trailing_group_id=1, trigger_percentage=Decimal("-1"))


def test_partial_group_valid() -> None:
    group = m.PartialGroup(user_id=1, name="Default")
    assert group.status is True


def test_partial_rule_valid_and_boundary_close_percentage() -> None:
    rule = m.PartialRule(
        name="Rule 1",
        partial_group_id=1,
        profit_percentage=Decimal("10"),
        close_percentage=Decimal("100"),
    )
    assert rule.close_percentage == Decimal("100")


def test_partial_rule_rejects_close_percentage_over_100() -> None:
    with pytest.raises(ValidationError):
        m.PartialRule(
            name="Rule 1",
            partial_group_id=1,
            profit_percentage=Decimal("10"),
            close_percentage=Decimal("101"),
        )


def test_partial_rule_rejects_zero_close_percentage() -> None:
    with pytest.raises(ValidationError):
        m.PartialRule(
            name="Rule 1",
            partial_group_id=1,
            profit_percentage=Decimal("10"),
            close_percentage=Decimal("0"),
        )


def test_action_group_valid() -> None:
    group = m.ActionGroup(user_id=1, name="Default")
    assert group.status is True


def test_action_valid_and_initial_data() -> None:
    action = m.Action(
        name="Default",
        action_group_id=1,
        asset_id=1,
        account_id=1,
        partial_group_id=1,
        trailing_group_id=1,
        risk_by_reward=Decimal("1"),
        take_profit=Decimal("1"),
        stop_loss=Decimal("1"),
    )
    assert action.status is True
    (record,) = m.Action.initial_data
    assert record["risk_by_reward"] == Decimal("1")


def test_position_valid_and_defaults() -> None:
    position = m.Position(
        user_id=1,
        name="Pos-1",
        trading_platform_id=1,
        broker_id=1,
        account_id=1,
        trailing_group_id=1,
        partial_group_id=1,
        action_group_id=1,
        action_id=1,
        date=datetime(2026, 1, 1, tzinfo=UTC),
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )
    assert position.is_executed is False
    assert position.profit == Decimal("0")


def test_position_rejects_non_positive_volume() -> None:
    with pytest.raises(ValidationError):
        m.Position(
            user_id=1,
            name="Pos-1",
            trading_platform_id=1,
            broker_id=1,
            account_id=1,
            trailing_group_id=1,
            partial_group_id=1,
            action_group_id=1,
            action_id=1,
            date=datetime(2026, 1, 1, tzinfo=UTC),
            volume=Decimal("0"),
            order_type="market",
            base_tp=Decimal("1"),
            base_sl=Decimal("1"),
            real_tp=Decimal("1"),
            real_sl=Decimal("1"),
        )
