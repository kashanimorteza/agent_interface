from __future__ import annotations

import datetime
import decimal

import model
import pytest
from cryptography.fernet import Fernet

from database import DatabaseInterface, config, mapping, observability
from database.adapter import StorageAdapter
from database.config import InstanceConfig, RuntimeConfig


@pytest.fixture(autouse=True)
def _encryption_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_ENCRYPTION_KEY", Fernet.generate_key().decode("ascii"))


@pytest.fixture(autouse=True)
def _clear_observability() -> None:
    observability.clear_events()
    yield
    observability.clear_events()


@pytest.fixture
def runtime_config() -> RuntimeConfig:
    return RuntimeConfig(
        instances={
            "general": InstanceConfig(
                key="general",
                name="Test General",
                purpose="Test data.",
                engine="sqlite",
                database="test_general",
            ),
            "secondary": InstanceConfig(
                key="secondary",
                name="Test Secondary",
                purpose="Test isolation.",
                engine="sqlite",
                database="test_secondary",
            ),
        },
        default_instance="general",
    )


@pytest.fixture
def adapter(
    tmp_path, monkeypatch: pytest.MonkeyPatch, runtime_config: RuntimeConfig
) -> StorageAdapter:
    monkeypatch.setattr(config, "DATA_DIRECTORY", tmp_path)
    adapter = StorageAdapter(runtime_config)
    mapping.METADATA.create_all(adapter.engine_for(None))
    mapping.METADATA.create_all(adapter.engine_for("secondary"))
    return adapter


@pytest.fixture
def db(adapter: StorageAdapter) -> DatabaseInterface:
    return DatabaseInterface(adapter)


@pytest.fixture
def graph(db: DatabaseInterface) -> dict[type[model.ModelFoundation], model.ModelFoundation]:
    """One persisted, valid instance of every one of the 15 Domain Definitions, created in
    dependency order — a ready-made fixture graph for tests that need a complete, referentially
    valid record of every mapped type."""
    created: dict[type[model.ModelFoundation], model.ModelFoundation] = {}

    user = db.create(
        model.User(name="Grapher", username="grapher", password="pw", api_key="key")
    )
    created[model.User] = user

    trading_platform = db.create(
        model.TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    )
    created[model.TradingPlatform] = trading_platform

    broker = db.create(model.Broker(name="GraphBroker", user_id=user.id))
    created[model.Broker] = broker

    instance = db.create(
        model.Instance(
            user_id=user.id,
            name="GraphInstance",
            trading_platform_id=trading_platform.id,
            password="pw",
            api_key="key",
        )
    )
    created[model.Instance] = instance

    currency = db.create(model.Currency(user_id=user.id, code="USD"))
    created[model.Currency] = currency

    asset = db.create(
        model.Asset(broker_id=broker.id, symbol="EUR/USD", category="Currency")
    )
    created[model.Asset] = asset

    account_group = db.create(model.AccountGroup(user_id=user.id, name="GraphGroup"))
    created[model.AccountGroup] = account_group

    account = db.create(
        model.Account(
            name="GraphAccount",
            group_id=account_group.id,
            broker_id=broker.id,
            instance_id=instance.id,
            base_currency_id=currency.id,
            username="acct",
            password="pw",
            leverage=100,
            account_type="CFD",
        )
    )
    created[model.Account] = account

    trailing_group = db.create(model.TrailingGroup(user_id=user.id, name="GraphTrailing"))
    created[model.TrailingGroup] = trailing_group

    trailing_rule = db.create(
        model.TrailingRule(
            name="GraphTrailingRule",
            trailing_group_id=trailing_group.id,
            trigger_percentage=decimal.Decimal("50"),
        )
    )
    created[model.TrailingRule] = trailing_rule

    partial_group = db.create(model.PartialGroup(user_id=user.id, name="GraphPartial"))
    created[model.PartialGroup] = partial_group

    partial_rule = db.create(
        model.PartialRule(
            name="GraphPartialRule",
            partial_group_id=partial_group.id,
            profit_percentage=decimal.Decimal("50"),
            close_percentage=decimal.Decimal("50"),
        )
    )
    created[model.PartialRule] = partial_rule

    action_group = db.create(model.ActionGroup(user_id=user.id, name="GraphAction"))
    created[model.ActionGroup] = action_group

    action = db.create(
        model.Action(
            name="GraphActionDef",
            action_group_id=action_group.id,
            asset_id=asset.id,
            account_id=account.id,
            partial_group_id=partial_group.id,
            trailing_group_id=trailing_group.id,
            risk_by_reward=decimal.Decimal("1"),
            take_profit=decimal.Decimal("1"),
            stop_loss=decimal.Decimal("1"),
        )
    )
    created[model.Action] = action

    position = db.create(
        model.Position(
            user_id=user.id,
            name="GraphPosition",
            trading_platform_id=trading_platform.id,
            broker_id=broker.id,
            account_id=account.id,
            trailing_group_id=trailing_group.id,
            partial_group_id=partial_group.id,
            action_group_id=action_group.id,
            action_id=action.id,
            date=datetime.datetime.now(datetime.UTC),
            volume=decimal.Decimal("1"),
            order_type="market",
            base_tp=decimal.Decimal("1"),
            base_sl=decimal.Decimal("1"),
            real_tp=decimal.Decimal("1"),
            real_sl=decimal.Decimal("1"),
        )
    )
    created[model.Position] = position

    return created
