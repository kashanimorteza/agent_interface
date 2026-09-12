"""Credential at-rest transformation (Task P2-T4)."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from my_database import _credentials

_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "trading_assistant_general.db"


def test_hash_round_trip_and_rejection():
    stored = _credentials.hash_value("correct horse battery staple")
    assert _credentials.verify_hash("correct horse battery staple", stored)
    assert not _credentials.verify_hash("wrong password", stored)
    assert stored != "correct horse battery staple"


def test_encryption_round_trip():
    stored = _credentials.encrypt_value("super-secret-api-key")
    assert stored != "super-secret-api-key"
    assert _credentials.decrypt_value(stored) == "super-secret-api-key"


def test_decrypt_rejects_tampered_value():
    with pytest.raises(ValueError):
        _credentials.decrypt_value("not-a-real-fernet-token")


def test_field_mode_resolution():
    assert _credentials.credential_mode("password") == "hash"
    assert _credentials.credential_mode("api_key") == "encrypted"


def test_seeded_admin_credentials_are_transformed_at_rest():
    conn = sqlite3.connect(_DB_PATH)
    try:
        password, api_key = conn.execute(
            "select password, api_key from users where name = 'Admin'"
        ).fetchone()
    finally:
        conn.close()
    assert password.startswith("pbkdf2_sha256$")
    assert api_key != "admin"
    assert len(api_key) > 20
