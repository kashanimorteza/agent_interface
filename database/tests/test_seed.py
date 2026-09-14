"""Tests for declared Initial Data seeding (task P2-G10-T1)."""

from __future__ import annotations

import model

from database.seed import seed_initial_data


def test_seeding_creates_every_target_declared_initial_record(db) -> None:
    seed_initial_data(db)

    users = db.list(model.User, name="Admin")
    assert len(users) == 1
    admin = users[0]
    assert admin.username == "admin"
    assert admin.password != ""  # protected, not empty
    assert admin.password not in ("change-me",)

    platforms = {p.code for p in db.list(model.TradingPlatform)}
    assert platforms == {"metatrader_5", "binance"}

    assert len(db.list(model.Instance, user_id=admin.id)) == 1
    assert len(db.list(model.Currency, user_id=admin.id)) == 8
    assert len(db.list(model.Broker, user_id=admin.id)) == 1

    brokers = db.list(model.Broker, user_id=admin.id)
    assert len(db.list(model.Asset, broker_id=brokers[0].id)) == 4

    assert len(db.list(model.AccountGroup, user_id=admin.id)) == 1
    assert len(db.list(model.Account, name="Acc-1")) == 1
    assert len(db.list(model.TrailingGroup, user_id=admin.id)) == 1
    assert len(db.list(model.PartialGroup, user_id=admin.id)) == 1
    assert len(db.list(model.ActionGroup, user_id=admin.id)) == 1
    assert len(db.list(model.Action, name="Default")) == 1

    # No initial data declared for these; seeding never invents any.
    assert db.list(model.TrailingRule) == ()
    assert db.list(model.PartialRule) == ()
    assert db.list(model.Position) == ()


def test_seeding_generated_credentials_are_never_stored_as_plaintext(db) -> None:
    seed_initial_data(db)
    admin = db.list(model.User, name="Admin")[0]
    # The Database Interface never returns a usable credential representation.
    assert admin.password == "***protected***"
    assert admin.api_key == "***protected***"

    # At the storage layer itself (not just the interface), the values are transformed,
    # not the caller-generated plaintext.
    from database.mapping.identity import UserTable

    session = db.adapter.session()
    row = session.get(UserTable, admin.id)
    assert row is not None
    assert row.password.startswith("pbkdf2$")  # User.password resolves to hash mode
    assert row.api_key.startswith("pbkdf2$")  # User.api_key resolves to hash mode
    session.close()


def test_seeding_is_repeatable_without_duplicates_or_uniqueness_violations(db) -> None:
    seed_initial_data(db)
    seed_initial_data(db)  # must not raise, and must not duplicate

    assert len(db.list(model.User, name="Admin")) == 1
    assert len(db.list(model.TradingPlatform)) == 2
    assert len(db.list(model.Currency)) == 8
    assert len(db.list(model.Asset)) == 4
    assert len(db.list(model.Account, name="Acc-1")) == 1
    assert len(db.list(model.Action, name="Default")) == 1


def test_seeding_returns_generated_credentials_exactly_once(db) -> None:
    first = seed_initial_data(db)
    assert set(first) == {
        "admin_password",
        "admin_api_key",
        "instance_password",
        "instance_api_key",
        "account_password",
    }
    for value in first.values():
        assert value and value != "***protected***"

    second = seed_initial_data(db)
    assert second == {}
    for value in first.values():
        assert value not in second.values()
