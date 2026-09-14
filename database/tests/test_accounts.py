import pytest
from model import (
    Account,
    AccountGroup,
    Broker,
    Currency,
    Instance,
    TradingPlatform,
    User,
)
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, transaction


def _make_account_dependencies(tx):
    user = create(
        User(name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")),
        session=tx,
    )
    platform = create(
        TradingPlatform(name="MetaTrader 5", code="metatrader_5"), session=tx
    )
    assert user.id is not None and platform.id is not None
    group = create(AccountGroup(user_id=user.id, name="Default"), session=tx)
    broker = create(Broker(name="FxPro", user_id=user.id), session=tx)
    instance = create(
        Instance(user_id=user.id, name="Conn", trading_platform_id=platform.id),
        session=tx,
    )
    currency = create(Currency(user_id=user.id, code="USD"), session=tx)
    assert (
        group.id is not None
        and broker.id is not None
        and instance.id is not None
        and currency.id is not None
    )
    return group.id, broker.id, instance.id, currency.id


def test_account_group_rejects_duplicate_per_user_name():
    with transaction() as tx:
        user = create(
            User(
                name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")
            ),
            session=tx,
        )
        assert user.id is not None
        create(AccountGroup(user_id=user.id, name="Default"), session=tx)
        user_id = user.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(AccountGroup(user_id=user_id, name="Default"), session=tx)


def test_account_persists_protects_password_and_enforces_uniqueness():
    with transaction() as tx:
        group_id, broker_id, instance_id, currency_id = _make_account_dependencies(tx)
        account = create(
            Account(
                name="Acc-1",
                group_id=group_id,
                broker_id=broker_id,
                instance_id=instance_id,
                base_currency_id=currency_id,
                username="test",
                password=SecretStr("secret"),
                leverage=100,
                account_type="CFD",
            ),
            session=tx,
        )
        assert account.password.get_secret_value() == "secret"
        args = (group_id, broker_id, instance_id, currency_id)

    with pytest.raises(IntegrityError), transaction() as tx:
        group_id, broker_id, instance_id, currency_id = args
        create(
            Account(
                name="Acc-2",
                group_id=group_id,
                broker_id=broker_id,
                instance_id=instance_id,
                base_currency_id=currency_id,
                username="test2",
                password=SecretStr("secret2"),
                leverage=50,
                account_type="CFD",
            ),
            session=tx,
        )
