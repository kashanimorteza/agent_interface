"""Valid domain instances built bottom-up through the declared relationship graph."""

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from model import (
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


@pytest.fixture
def user() -> User:
    return User(
        id=1,
        name="Admin",
        username="admin",
        password="secret-password",
        api_key="secret-api-key",
    )


@pytest.fixture
def trading_platform() -> TradingPlatform:
    return TradingPlatform(id=1, name="MetaTrader 5", code="metatrader_5")


@pytest.fixture
def instance(user: User, trading_platform: TradingPlatform) -> Instance:
    return Instance(
        id=1,
        user_id=user.id,
        trading_platform_id=trading_platform.id,
        name="MetaTrader",
        ip="127.0.0.1",
        username="test",
        password="secret-password",
        api_key="secret-api-key",
    )


@pytest.fixture
def currency(user: User) -> Currency:
    return Currency(id=1, user_id=user.id, code="USD", symbol="$", country="United States")


@pytest.fixture
def broker(user: User) -> Broker:
    return Broker(id=1, name="FxPro", user_id=user.id)


@pytest.fixture
def asset(broker: Broker) -> Asset:
    return Asset(
        id=1,
        broker_id=broker.id,
        symbol="EUR/USD",
        category="Currency",
        point_size=0.0001,
        digits=5,
    )


@pytest.fixture
def account_group(user: User) -> AccountGroup:
    return AccountGroup(id=1, user_id=user.id, name="Default")


@pytest.fixture
def account(
    account_group: AccountGroup, broker: Broker, instance: Instance, currency: Currency
) -> Account:
    return Account(
        id=1,
        name="Acc-1",
        group_id=account_group.id,
        broker_id=broker.id,
        instance_id=instance.id,
        base_currency_id=currency.id,
        username="test",
        password="secret-password",
        leverage=100,
        account_type="CFD",
    )


@pytest.fixture
def trailing_group(user: User) -> TrailingGroup:
    return TrailingGroup(id=1, user_id=user.id, name="Default")


@pytest.fixture
def trailing_rule(trailing_group: TrailingGroup) -> TrailingRule:
    return TrailingRule(
        id=1,
        name="TR-1",
        trailing_group_id=trailing_group.id,
        trigger_percentage=Decimal("50"),
        take_profit_adjustment=Decimal("1.5"),
        stop_loss_adjustment=Decimal("0.5"),
    )


@pytest.fixture
def partial_group(user: User) -> PartialGroup:
    return PartialGroup(id=1, user_id=user.id, name="Default")


@pytest.fixture
def partial_rule(partial_group: PartialGroup) -> PartialRule:
    return PartialRule(
        id=1,
        name="PR-1",
        partial_group_id=partial_group.id,
        profit_percentage=Decimal("50"),
        close_percentage=Decimal("25"),
    )


@pytest.fixture
def action_group(user: User) -> ActionGroup:
    return ActionGroup(id=1, user_id=user.id, name="Default")


@pytest.fixture
def action(
    action_group: ActionGroup,
    asset: Asset,
    account: Account,
    partial_group: PartialGroup,
    trailing_group: TrailingGroup,
) -> Action:
    return Action(
        id=1,
        name="Default",
        action_group_id=action_group.id,
        asset_id=asset.id,
        account_id=account.id,
        partial_group_id=partial_group.id,
        trailing_group_id=trailing_group.id,
        risk_by_reward=Decimal("1"),
        take_profit=Decimal("1"),
        stop_loss=Decimal("1"),
    )


@pytest.fixture
def position(
    user: User,
    trading_platform: TradingPlatform,
    broker: Broker,
    account: Account,
    trailing_group: TrailingGroup,
    partial_group: PartialGroup,
    action_group: ActionGroup,
    action: Action,
) -> Position:
    return Position(
        id=1,
        user_id=user.id,
        name="Pos-1",
        trading_platform_id=trading_platform.id,
        broker_id=broker.id,
        account_id=account.id,
        trailing_group_id=trailing_group.id,
        partial_group_id=partial_group.id,
        action_group_id=action_group.id,
        action_id=action.id,
        date=datetime(2026, 1, 1, tzinfo=UTC),
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )
