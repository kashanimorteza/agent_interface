"""Reads never expose the storage representation of a credential."""

from __future__ import annotations

from my_model.instance import Instance
from my_model.trading_platform import TradingPlatform
from my_model.user import User

from my_database import interface
from my_database._convert import REDACTED


def test_hash_mode_credential_is_redacted_on_read():
    created = interface.add(
        User(name="Ada", username="ada", password="secret", api_key="key")
    )
    assert created.id is not None
    fetched = interface.get(User, created.id)
    assert fetched is not None
    assert fetched.password == REDACTED
    assert fetched.api_key == REDACTED
    assert fetched.password != "secret"


def test_encrypted_mode_credential_is_recoverable_on_read():
    user = interface.add(User(name="Ada", username="ada", password="x", api_key="y"))
    assert user.id is not None
    platform = interface.add(TradingPlatform(name="MetaTrader 5", code="metatrader_5"))
    assert platform.id is not None
    created = interface.add(
        Instance(
            user_id=user.id,
            name="MetaTrader",
            trading_platform_id=platform.id,
            password="conn-secret",
        )
    )
    assert created.id is not None
    fetched = interface.get(Instance, created.id)
    assert fetched is not None
    assert fetched.password == "conn-secret"


def test_storage_representation_never_appears_in_a_read_result():
    interface.add(
        User(name="Bob", username="bob", password="hunter2", api_key="apikey123")
    )
    all_users = interface.list_(User)
    for u in all_users:
        assert u.password != "hunter2" or u.password == REDACTED
        assert "hunter2" not in (u.password or "")
