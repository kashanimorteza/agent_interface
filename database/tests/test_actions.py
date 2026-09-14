from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol

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
    Position,
    TradingPlatform,
    TrailingGroup,
    User,
)
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, transaction


class _HasId(Protocol):
    id: int | None


def _id(row: _HasId) -> int:
    assert row.id is not None
    return row.id


def _full_dependency_set(tx):
    user = create(
        User(name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")),
        session=tx,
    )
    platform = create(
        TradingPlatform(name="MetaTrader 5", code="metatrader_5"), session=tx
    )
    broker = create(Broker(name="FxPro", user_id=_id(user)), session=tx)
    instance = create(
        Instance(user_id=_id(user), name="Conn", trading_platform_id=_id(platform)),
        session=tx,
    )
    currency = create(Currency(user_id=_id(user), code="USD"), session=tx)
    group = create(AccountGroup(user_id=_id(user), name="Default"), session=tx)
    account = create(
        Account(
            name="Acc-1",
            group_id=_id(group),
            broker_id=_id(broker),
            instance_id=_id(instance),
            base_currency_id=_id(currency),
            username="t",
            password=SecretStr("s"),
            leverage=100,
            account_type="CFD",
        ),
        session=tx,
    )
    asset = create(
        Asset(broker_id=_id(broker), symbol="EUR/USD", category="Currency"), session=tx
    )
    partial_group = create(PartialGroup(user_id=_id(user), name="Default"), session=tx)
    trailing_group = create(
        TrailingGroup(user_id=_id(user), name="Default"), session=tx
    )
    action_group = create(ActionGroup(user_id=_id(user), name="Default"), session=tx)
    return {
        "user": _id(user),
        "platform": _id(platform),
        "broker": _id(broker),
        "account": _id(account),
        "asset": _id(asset),
        "partial_group": _id(partial_group),
        "trailing_group": _id(trailing_group),
        "action_group": _id(action_group),
    }


def test_action_group_rejects_duplicate_per_user_name():
    with transaction() as tx:
        user = create(
            User(
                name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")
            ),
            session=tx,
        )
        create(ActionGroup(user_id=_id(user), name="Default"), session=tx)
        user_id = _id(user)

    with pytest.raises(IntegrityError), transaction() as tx:
        create(ActionGroup(user_id=user_id, name="Default"), session=tx)


def test_action_persists_and_enforces_per_group_name_uniqueness():
    with transaction() as tx:
        ids = _full_dependency_set(tx)
        create(
            Action(
                name="Default",
                action_group_id=ids["action_group"],
                asset_id=ids["asset"],
                account_id=ids["account"],
                partial_group_id=ids["partial_group"],
                trailing_group_id=ids["trailing_group"],
                risk_by_reward=Decimal(1),
                take_profit=Decimal(1),
                stop_loss=Decimal(1),
            ),
            session=tx,
        )

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            Action(
                name="Default",
                action_group_id=ids["action_group"],
                asset_id=ids["asset"],
                account_id=ids["account"],
                partial_group_id=ids["partial_group"],
                trailing_group_id=ids["trailing_group"],
                risk_by_reward=Decimal(2),
                take_profit=Decimal(2),
                stop_loss=Decimal(2),
            ),
            session=tx,
        )


def test_position_rejects_nonexistent_relationship():
    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            Position(
                user_id=999,
                name="P1",
                trading_platform_id=999,
                broker_id=999,
                account_id=999,
                trailing_group_id=999,
                partial_group_id=999,
                action_group_id=999,
                action_id=999,
                date=datetime.now(UTC),
                volume=Decimal(1),
                order_type="market",
                base_tp=Decimal(1),
                base_sl=Decimal(1),
                real_tp=Decimal(1),
                real_sl=Decimal(1),
            ),
            session=tx,
        )


def test_position_persists_timezone_aware_date_and_enforces_display_name_uniqueness():
    with transaction() as tx:
        ids = _full_dependency_set(tx)
        action = create(
            Action(
                name="Default",
                action_group_id=ids["action_group"],
                asset_id=ids["asset"],
                account_id=ids["account"],
                partial_group_id=ids["partial_group"],
                trailing_group_id=ids["trailing_group"],
                risk_by_reward=Decimal(1),
                take_profit=Decimal(1),
                stop_loss=Decimal(1),
            ),
            session=tx,
        )
        when = datetime.now(UTC)
        position = create(
            Position(
                user_id=ids["user"],
                name="Pos-1",
                trading_platform_id=ids["platform"],
                broker_id=ids["broker"],
                account_id=ids["account"],
                trailing_group_id=ids["trailing_group"],
                partial_group_id=ids["partial_group"],
                action_group_id=ids["action_group"],
                action_id=_id(action),
                date=when,
                volume=Decimal(1),
                order_type="market",
                base_tp=Decimal(1),
                base_sl=Decimal(1),
                real_tp=Decimal(1),
                real_sl=Decimal(1),
            ),
            session=tx,
        )
        assert position.date == when
        assert position.date.tzinfo is not None
        action_id = _id(action)

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            Position(
                user_id=ids["user"],
                name="Pos-1",
                trading_platform_id=ids["platform"],
                broker_id=ids["broker"],
                account_id=ids["account"],
                trailing_group_id=ids["trailing_group"],
                partial_group_id=ids["partial_group"],
                action_group_id=ids["action_group"],
                action_id=action_id,
                date=datetime.now(UTC),
                volume=Decimal(1),
                order_type="market",
                base_tp=Decimal(1),
                base_sl=Decimal(1),
                real_tp=Decimal(1),
                real_sl=Decimal(1),
            ),
            session=tx,
        )
