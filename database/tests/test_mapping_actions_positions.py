"""Tests for the Actions and Positions storage mappings (tasks P2-G7-T1..T3)."""

from __future__ import annotations

import datetime
from decimal import Decimal

import model
import pytest
from sqlalchemy.exc import StatementError

from database.exceptions import ConstraintViolation
from database.mapping.actions_positions import PositionTable


def _build_full_chain(db):
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    platform = db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    instance = db.create(
        model.Instance(user_id=user.id, name="MetaTrader", trading_platform_id=platform.id)
    )
    broker = db.create(model.Broker(name="FxPro", user_id=user.id))
    currency = db.create(model.Currency(user_id=user.id, code="USD"))
    asset = db.create(model.Asset(broker_id=broker.id, symbol="EUR/USD", category="Currency"))
    account_group = db.create(model.AccountGroup(user_id=user.id, name="Default"))
    account = db.create(
        model.Account(
            name="Acc-1",
            group_id=account_group.id,
            broker_id=broker.id,
            instance_id=instance.id,
            base_currency_id=currency.id,
            username="test",
            password="secret",
            leverage=100,
            account_type="CFD",
        )
    )
    partial_group = db.create(model.PartialGroup(user_id=user.id, name="Default"))
    trailing_group = db.create(model.TrailingGroup(user_id=user.id, name="Default"))
    action_group = db.create(model.ActionGroup(user_id=user.id, name="Default"))
    return {
        "user": user,
        "platform": platform,
        "broker": broker,
        "account": account,
        "asset": asset,
        "partial_group": partial_group,
        "trailing_group": trailing_group,
        "action_group": action_group,
    }


def test_action_group_mapping_preserves_fields_relationship_and_uniqueness(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    created = db.create(model.ActionGroup(user_id=user.id, name="Default"))
    fetched = db.get(model.ActionGroup, created.id)
    assert fetched is not None
    assert fetched.name == "Default"

    with pytest.raises(ConstraintViolation):
        db.create(model.ActionGroup(user_id=user.id, name="Default"))


def test_action_mapping_preserves_fields_relationships_and_uniqueness(db) -> None:
    chain = _build_full_chain(db)
    created = db.create(
        model.Action(
            name="Default",
            action_group_id=chain["action_group"].id,
            asset_id=chain["asset"].id,
            account_id=chain["account"].id,
            partial_group_id=chain["partial_group"].id,
            trailing_group_id=chain["trailing_group"].id,
            risk_by_reward=Decimal("1"),
            take_profit=Decimal("1"),
            stop_loss=Decimal("1"),
        )
    )
    fetched = db.get(model.Action, created.id)
    assert fetched is not None
    assert fetched.action_group_id == chain["action_group"].id
    assert fetched.asset_id == chain["asset"].id
    assert fetched.account_id == chain["account"].id

    with pytest.raises(ConstraintViolation):
        db.create(
            model.Action(
                name="Default",
                action_group_id=chain["action_group"].id,
                asset_id=chain["asset"].id,
                account_id=chain["account"].id,
                partial_group_id=chain["partial_group"].id,
                trailing_group_id=chain["trailing_group"].id,
                risk_by_reward=Decimal("1"),
                take_profit=Decimal("1"),
                stop_loss=Decimal("1"),
            )
        )


def test_position_mapping_preserves_fields_relationships_uniqueness_and_timezone_rule(db) -> None:
    chain = _build_full_chain(db)
    action = db.create(
        model.Action(
            name="Default",
            action_group_id=chain["action_group"].id,
            asset_id=chain["asset"].id,
            account_id=chain["account"].id,
            partial_group_id=chain["partial_group"].id,
            trailing_group_id=chain["trailing_group"].id,
            risk_by_reward=Decimal("1"),
            take_profit=Decimal("1"),
            stop_loss=Decimal("1"),
        )
    )

    created = db.create(
        model.Position(
            user_id=chain["user"].id,
            name="Pos-1",
            trading_platform_id=chain["platform"].id,
            broker_id=chain["broker"].id,
            account_id=chain["account"].id,
            trailing_group_id=chain["trailing_group"].id,
            partial_group_id=chain["partial_group"].id,
            action_group_id=chain["action_group"].id,
            action_id=action.id,
            date=datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC),
            volume=Decimal("1"),
            order_type="market",
            base_tp=Decimal("1"),
            base_sl=Decimal("1"),
            real_tp=Decimal("1"),
            real_sl=Decimal("1"),
        )
    )
    fetched = db.get(model.Position, created.id)
    assert fetched is not None
    assert fetched.name == "Pos-1"
    assert fetched.date.tzinfo is not None

    with pytest.raises(ConstraintViolation):
        db.create(
            model.Position(
                user_id=chain["user"].id,
                name="Pos-1",
                trading_platform_id=chain["platform"].id,
                broker_id=chain["broker"].id,
                account_id=chain["account"].id,
                trailing_group_id=chain["trailing_group"].id,
                partial_group_id=chain["partial_group"].id,
                action_group_id=chain["action_group"].id,
                action_id=action.id,
                date=datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
                volume=Decimal("1"),
                order_type="market",
                base_tp=Decimal("1"),
                base_sl=Decimal("1"),
                real_tp=Decimal("1"),
                real_sl=Decimal("1"),
            )
        )


def test_storage_layer_itself_rejects_a_naive_datetime(db) -> None:
    """Database's own UTCDateTime column type rejects a naive datetime independently of
    Model's own validation, proving the storage mapping enforces the rule itself."""
    row = PositionTable(
        user_id=1,
        name="Direct-Row",
        trading_platform_id=1,
        broker_id=1,
        account_id=1,
        trailing_group_id=1,
        partial_group_id=1,
        action_group_id=1,
        action_id=1,
        date=datetime.datetime(2026, 1, 1),  # naive
        volume=Decimal("1"),
        order_type="market",
        base_tp=Decimal("1"),
        base_sl=Decimal("1"),
        real_tp=Decimal("1"),
        real_sl=Decimal("1"),
    )
    session = db.adapter.session()
    session.add(row)
    with pytest.raises(StatementError, match="timezone-aware"):
        session.flush()
    session.rollback()
    session.close()
