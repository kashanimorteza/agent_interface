import pytest
from pydantic import SecretStr, ValidationError

from model import Instance, TradingPlatform, User


def test_user_accepts_valid_data_and_protects_credentials():
    user = User(
        name="Admin",
        username="admin",
        password=SecretStr("secret"),
        api_key=SecretStr("key123"),
    )
    assert "secret" not in str(user)
    assert "secret" not in repr(user)
    assert "key123" not in str(user)
    assert user.password.get_secret_value() == "secret"


def test_user_declares_display_name_uniqueness_metadata():
    assert User.unique_together == (("name",),)


def test_trading_platform_accepts_every_required_field():
    platform = TradingPlatform(name="MetaTrader 5", code="metatrader_5")
    assert platform.is_active is True


def test_trading_platform_rejects_missing_required_field():
    with pytest.raises(ValidationError):
        TradingPlatform.model_validate({"name": "MetaTrader 5"})


def test_instance_accepts_valid_data_and_protects_credentials():
    instance = Instance(
        user_id=1,
        name="MetaTrader",
        trading_platform_id=1,
        ip="127.0.0.1",
        username="test",
        password=SecretStr("secret"),
        api_key=SecretStr("key123"),
    )
    assert "secret" not in str(instance)
    assert instance.password is not None
    assert instance.password.get_secret_value() == "secret"


def test_instance_allows_omitted_optional_connection_fields():
    instance = Instance(user_id=1, name="MetaTrader", trading_platform_id=1)
    assert instance.ip is None
    assert instance.username is None
    assert instance.password is None
    assert instance.api_key is None


def test_instance_declares_per_user_name_uniqueness_metadata():
    assert Instance.unique_together == (("user_id", "name"),)
