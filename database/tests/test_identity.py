import pytest
from model import Instance, TradingPlatform, User
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, transaction


def test_duplicate_user_name_is_rejected():
    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            User(
                name="Dup",
                username="a",
                password=SecretStr("p"),
                api_key=SecretStr("k"),
            ),
            session=tx,
        )
        create(
            User(
                name="Dup",
                username="b",
                password=SecretStr("p2"),
                api_key=SecretStr("k2"),
            ),
            session=tx,
        )


def test_trading_platform_persists_and_retrieves_every_field():
    with transaction() as tx:
        platform = create(TradingPlatform(name="Binance", code="binance"), session=tx)
        assert platform.name == "Binance"
        assert platform.code == "binance"
        assert platform.is_active is True


def test_instance_rejects_nonexistent_user_or_platform():
    with pytest.raises(IntegrityError), transaction() as tx:
        create(Instance(user_id=999, name="X", trading_platform_id=999), session=tx)


def test_instance_rejects_duplicate_per_user_name():
    with transaction() as tx:
        user = create(
            User(
                name="U", username="u", password=SecretStr("p"), api_key=SecretStr("k")
            ),
            session=tx,
        )
        platform = create(
            TradingPlatform(name="MetaTrader 5", code="metatrader_5"), session=tx
        )
        assert user.id is not None
        assert platform.id is not None
        create(
            Instance(user_id=user.id, name="Conn", trading_platform_id=platform.id),
            session=tx,
        )
        user_id, platform_id = user.id, platform.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            Instance(user_id=user_id, name="Conn", trading_platform_id=platform_id),
            session=tx,
        )
