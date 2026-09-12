"""Credential storage transformations and the Model-declaration precedence
rule: an explicit Model-declared storage mode always wins over Database's
own generic field-name defaults.
"""

import my_model

import my_database
from my_database import _orm
from my_database._session import get_session_factory


def test_hash_credential_is_irreversible_and_redacted_on_read() -> None:
    created = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="secret", api_key="key")
    )
    with get_session_factory()() as session:
        row = session.get(_orm.UserRow, created.id)
        assert row is not None
        assert row.password != "secret"  # never stored in plaintext
        assert "$" in row.password  # our hash format marker

    fetched = my_database.read(my_model.User, created.id)
    assert fetched.password == "<redacted>"


def test_encrypted_credential_round_trips_to_the_original_value() -> None:
    user = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="y")
    )
    platform = my_database.add(my_model.TradingPlatform(id=0, name="MT5", code="metatrader_5"))
    created = my_database.add(
        my_model.Instance(
            id=0,
            user_id=user.id,
            name="MT",
            trading_platform_id=platform.id,
            password="connection-secret",
        )
    )
    with get_session_factory()() as session:
        row = session.get(_orm.InstanceRow, created.id)
        assert row is not None
        assert row.password != "connection-secret"

    fetched = my_database.read(my_model.Instance, created.id)
    assert fetched.password == "connection-secret"


def test_explicit_model_declared_hash_beats_the_generic_api_key_encrypted_default() -> None:
    """User.api_key is explicitly declared 'hash' by the Model even though
    Database's own generic field-name default for api_key is 'encrypted'.
    The explicit Model declaration must win.
    """
    created = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="secret-key")
    )
    with get_session_factory()() as session:
        row = session.get(_orm.UserRow, created.id)
        assert row is not None
        # A hash never round-trips to the original value; an encrypted value would.
        assert "$" in row.api_key
        assert row.api_key != "secret-key"

    fetched = my_database.read(my_model.User, created.id)
    assert fetched.api_key == "<redacted>"  # redacted (hash), never decrypted
