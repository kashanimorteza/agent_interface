from model import Instance, TradingPlatform, User
from pydantic import SecretStr

from database import create, get_by_id, transaction


def test_one_way_credential_never_reproduces_the_original_value():
    with transaction() as tx:
        user = create(
            User(
                name="A",
                username="a",
                password=SecretStr("plain-pw"),
                api_key=SecretStr("plain-key"),
            ),
            session=tx,
        )
        assert user.id is not None
        reread = get_by_id(User, user.id, session=tx)
        assert reread is not None
        assert reread.password.get_secret_value() != "plain-pw"
        assert reread.api_key.get_secret_value() != "plain-key"


def test_reversible_credential_always_reproduces_the_original_value():
    with transaction() as tx:
        user = create(
            User(
                name="B", username="b", password=SecretStr("x"), api_key=SecretStr("y")
            ),
            session=tx,
        )
        platform = create(
            TradingPlatform(name="MetaTrader 5", code="metatrader_5"), session=tx
        )
        assert user.id is not None
        assert platform.id is not None

        instance = create(
            Instance(
                user_id=user.id,
                name="Conn",
                trading_platform_id=platform.id,
                password=SecretStr("technical-secret"),
                api_key=SecretStr("technical-key"),
            ),
            session=tx,
        )
        assert instance.id is not None
        reread = get_by_id(Instance, instance.id, session=tx)
        assert reread is not None
        assert reread.password is not None
        assert reread.password.get_secret_value() == "technical-secret"
        assert reread.api_key is not None
        assert reread.api_key.get_secret_value() == "technical-key"
