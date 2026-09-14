import pytest
from model import Asset, Broker, Currency, User
from pydantic import SecretStr
from sqlalchemy.exc import IntegrityError

from database import create, transaction


def _make_user(tx, name: str = "U") -> int:
    user = create(
        User(
            name=name,
            username=name.lower(),
            password=SecretStr("p"),
            api_key=SecretStr("k"),
        ),
        session=tx,
    )
    assert user.id is not None
    return user.id


def test_currency_rejects_nonexistent_user():
    with pytest.raises(IntegrityError), transaction() as tx:
        create(Currency(user_id=999, code="USD"), session=tx)


def test_currency_rejects_duplicate_per_user_code():
    with transaction() as tx:
        user_id = _make_user(tx)
        create(Currency(user_id=user_id, code="USD"), session=tx)

    with pytest.raises(IntegrityError), transaction() as tx:
        create(Currency(user_id=user_id, code="USD"), session=tx)


def test_broker_rejects_duplicate_per_user_name():
    with transaction() as tx:
        user_id = _make_user(tx)
        create(Broker(name="FxPro", user_id=user_id), session=tx)

    with pytest.raises(IntegrityError), transaction() as tx:
        create(Broker(name="FxPro", user_id=user_id), session=tx)


def test_asset_rejects_duplicate_per_broker_symbol():
    with transaction() as tx:
        user_id = _make_user(tx)
        broker = create(Broker(name="FxPro", user_id=user_id), session=tx)
        assert broker.id is not None
        create(
            Asset(broker_id=broker.id, symbol="EUR/USD", category="Currency"),
            session=tx,
        )
        broker_id = broker.id

    with pytest.raises(IntegrityError), transaction() as tx:
        create(
            Asset(broker_id=broker_id, symbol="EUR/USD", category="Currency"),
            session=tx,
        )
