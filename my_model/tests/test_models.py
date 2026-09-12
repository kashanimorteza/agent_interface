from datetime import datetime, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from my_model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from my_model import account as account_module
from my_model import account_group as account_group_module
from my_model import action as action_module
from my_model import action_group as action_group_module
from my_model import asset as asset_module
from my_model import broker as broker_module
from my_model import currency as currency_module
from my_model import instance as instance_module
from my_model import partial_group as partial_group_module
from my_model import partial_rule as partial_rule_module
from my_model import position as position_module
from my_model import trading_platform as trading_platform_module
from my_model import trailing_group as trailing_group_module
from my_model import trailing_rule as trailing_rule_module
from my_model import user as user_module


def assert_rejects_unexpected_field(instance: object, cls: type) -> None:
    data = instance.model_dump()  # type: ignore[attr-defined]
    data["totally_unexpected_field"] = "x"
    with pytest.raises(ValidationError):
        cls.model_validate(data)


# --- User -------------------------------------------------------------------


def test_user_valid_and_rejects_unexpected_field() -> None:
    user = User(name="Ada", username="ada", password="secret", api_key="key")
    assert user.status is True
    assert_rejects_unexpected_field(user, User)


def test_user_initial_data_matches_target() -> None:
    assert len(user_module.INITIAL_DATA) == 1
    record = user_module.INITIAL_DATA[0]
    assert record["name"] == "Admin"
    assert record["username"] == "admin"


# --- Trading Platform ---------------------------------------------------------


def test_trading_platform_valid_and_rejects_unexpected_field() -> None:
    platform = TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    assert_rejects_unexpected_field(platform, TradingPlatform)


def test_trading_platform_initial_data_matches_target() -> None:
    codes = {record["code"] for record in trading_platform_module.INITIAL_DATA}
    assert codes == {"metatrader_5", "binance"}


# --- Instance -----------------------------------------------------------------


def test_instance_valid_and_rejects_unexpected_field() -> None:
    instance = Instance(user_id=1, name="MetaTrader", trading_platform_id=1)
    assert instance.ip is None
    assert_rejects_unexpected_field(instance, Instance)


def test_instance_initial_data_matches_target() -> None:
    assert len(instance_module.INITIAL_DATA) == 1
    record = instance_module.INITIAL_DATA[0]
    assert record["name"] == "MetaTrader"
    assert record["ip"] == "127.0.0.1"


# --- Currency -------------------------------------------------------------------


def test_currency_valid_and_rejects_unexpected_field() -> None:
    currency = Currency(user_id=1, code="USD")
    assert currency.decimal_digits == 2
    assert_rejects_unexpected_field(currency, Currency)


def test_currency_code_must_be_three_letters() -> None:
    with pytest.raises(ValidationError):
        Currency(user_id=1, code="US")


def test_currency_initial_data_matches_target() -> None:
    codes = [record["code"] for record in currency_module.INITIAL_DATA]
    assert codes == ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "NZD"]


# --- Broker ---------------------------------------------------------------------


def test_broker_valid_and_rejects_unexpected_field() -> None:
    broker = Broker(name="FxPro", user_id=1)
    assert_rejects_unexpected_field(broker, Broker)


def test_broker_initial_data_matches_target() -> None:
    assert broker_module.INITIAL_DATA == [{"name": "FxPro", "user_id": 1}]


# --- Asset ----------------------------------------------------------------------


def test_asset_valid_and_rejects_unexpected_field() -> None:
    asset = Asset(broker_id=1, symbol="EUR/USD", category="Currency")
    assert_rejects_unexpected_field(asset, Asset)


def test_asset_initial_data_matches_target() -> None:
    symbols = {record["symbol"] for record in asset_module.INITIAL_DATA}
    assert symbols == {"EUR/USD", "EUR/GBP", "XAU/USD", "USOil"}


# --- Account Group ----------------------------------------------------------------


def test_account_group_valid_and_rejects_unexpected_field() -> None:
    group = AccountGroup(user_id=1, name="Default")
    assert_rejects_unexpected_field(group, AccountGroup)


def test_account_group_initial_data_matches_target() -> None:
    assert account_group_module.INITIAL_DATA == [{"user_id": 1, "name": "Default"}]


# --- Account --------------------------------------------------------------------


def test_account_valid_and_rejects_unexpected_field() -> None:
    account = Account(
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
    assert account.balance == Decimal(0)
    assert_rejects_unexpected_field(account, Account)


def test_account_initial_data_matches_target() -> None:
    assert len(account_module.INITIAL_DATA) == 1
    assert account_module.INITIAL_DATA[0]["name"] == "Acc-1"


# --- Trailing Group ---------------------------------------------------------------


def test_trailing_group_valid_and_rejects_unexpected_field() -> None:
    group = TrailingGroup(user_id=1, name="Default")
    assert_rejects_unexpected_field(group, TrailingGroup)


def test_trailing_group_initial_data_matches_target() -> None:
    assert trailing_group_module.INITIAL_DATA == [{"user_id": 1, "name": "Default"}]


# --- Trailing Rule ------------------------------------------------------------------


def test_trailing_rule_valid_and_rejects_unexpected_field() -> None:
    rule = TrailingRule(name="Rule", trailing_group_id=1, trigger_percentage=Decimal("50"))
    assert rule.take_profit_adjustment is None
    assert_rejects_unexpected_field(rule, TrailingRule)


def test_trailing_rule_percentage_must_stay_within_bounds() -> None:
    with pytest.raises(ValidationError):
        TrailingRule(name="Rule", trailing_group_id=1, trigger_percentage=Decimal("150"))


def test_trailing_rule_declares_no_initial_data() -> None:
    assert trailing_rule_module.INITIAL_DATA == []


# --- Partial Group --------------------------------------------------------------------


def test_partial_group_valid_and_rejects_unexpected_field() -> None:
    group = PartialGroup(user_id=1, name="Default")
    assert_rejects_unexpected_field(group, PartialGroup)


def test_partial_group_initial_data_matches_target() -> None:
    assert partial_group_module.INITIAL_DATA == [{"user_id": 1, "name": "Default"}]


# --- Partial Rule ------------------------------------------------------------------------


def test_partial_rule_valid_and_rejects_unexpected_field() -> None:
    rule = PartialRule(
        name="Rule",
        partial_group_id=1,
        profit_percentage=Decimal("10"),
        close_percentage=Decimal("50"),
    )
    assert_rejects_unexpected_field(rule, PartialRule)


def test_partial_rule_percentage_must_stay_within_bounds() -> None:
    with pytest.raises(ValidationError):
        PartialRule(
            name="Rule",
            partial_group_id=1,
            profit_percentage=Decimal("-1"),
            close_percentage=Decimal("50"),
        )


def test_partial_rule_declares_no_initial_data() -> None:
    assert partial_rule_module.INITIAL_DATA == []


# --- Action Group -----------------------------------------------------------------------


def test_action_group_valid_and_rejects_unexpected_field() -> None:
    group = ActionGroup(user_id=1, name="Default")
    assert_rejects_unexpected_field(group, ActionGroup)


def test_action_group_initial_data_matches_target() -> None:
    assert action_group_module.INITIAL_DATA == [{"user_id": 1, "name": "Default"}]


# --- Action ---------------------------------------------------------------------------------


def test_action_valid_and_rejects_unexpected_field() -> None:
    action = Action(
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
    assert_rejects_unexpected_field(action, Action)


def test_action_initial_data_matches_target() -> None:
    assert len(action_module.INITIAL_DATA) == 1
    assert action_module.INITIAL_DATA[0]["name"] == "Default"


# --- Position -------------------------------------------------------------------------------


def _valid_position_kwargs() -> dict[str, object]:
    return dict(
        user_id=1,
        name="Pos-1",
        trading_platform_id=1,
        broker_id=1,
        account_id=1,
        trailing_group_id=1,
        partial_group_id=1,
        action_group_id=1,
        action_id=1,
        date=datetime.now(timezone.utc),
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )


def test_position_valid_and_rejects_unexpected_field() -> None:
    position = Position(**_valid_position_kwargs())
    assert position.is_executed is False
    assert_rejects_unexpected_field(position, Position)


def test_position_requires_timezone_aware_date() -> None:
    kwargs = _valid_position_kwargs()
    kwargs["date"] = datetime.now()
    with pytest.raises(ValidationError):
        Position(**kwargs)


def test_position_declares_no_initial_data() -> None:
    assert position_module.INITIAL_DATA == []
