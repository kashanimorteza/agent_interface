"""Tests for Database.verify_credential (added for Backend's authentication need)."""

from __future__ import annotations

import model
import pytest


def test_verify_credential_returns_id_for_matching_active_user(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="secret-key"))
    matched_id = db.verify_credential(model.User, "api_key", "secret-key")
    assert matched_id == user.id


def test_verify_credential_returns_none_for_non_matching_candidate(db) -> None:
    db.create(model.User(name="Ada", username="ada", password="pw", api_key="secret-key"))
    assert db.verify_credential(model.User, "api_key", "wrong-key") is None


def test_verify_credential_excludes_inactive_records(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="secret-key"))
    db.activate(model.User, user.id, enable=False)
    assert db.verify_credential(model.User, "api_key", "secret-key") is None


def test_verify_credential_rejects_encrypted_mode_fields(db) -> None:
    with pytest.raises(ValueError, match="not a one-way-hashed"):
        db.verify_credential(model.Instance, "api_key", "anything")


def test_verify_credential_never_exposes_the_stored_hash(
    db, caplog: pytest.LogCaptureFixture
) -> None:
    db.create(model.User(name="Ada", username="ada", password="pw", api_key="secret-key"))
    caplog.set_level("INFO", logger="database.signals")
    result = db.verify_credential(model.User, "api_key", "secret-key")
    assert isinstance(result, int)
    for record in caplog.records:
        assert "secret-key" not in record.message
        assert "pbkdf2$" not in record.message
