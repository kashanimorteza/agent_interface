from __future__ import annotations

import pytest

from database import credentials
from database.credentials import MissingEncryptionKeyError


def test_hash_value_is_one_way_and_verifiable() -> None:
    stored = credentials.hash_value("s3cret!")
    assert stored != "s3cret!"
    assert credentials.verify_hash("s3cret!", stored)
    assert not credentials.verify_hash("wrong", stored)


def test_hash_value_uses_distinct_salt_per_call() -> None:
    a = credentials.hash_value("same-input")
    b = credentials.hash_value("same-input")
    assert a != b  # distinct salts
    assert credentials.verify_hash("same-input", a)
    assert credentials.verify_hash("same-input", b)


def test_encrypt_value_round_trips(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "DATABASE_ENCRYPTION_KEY", credentials.generate_encryption_key()
    )
    token = credentials.encrypt_value("api-secret-value")
    assert token != "api-secret-value"
    assert credentials.decrypt_value(token) == "api-secret-value"


def test_encrypt_value_requires_runtime_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_ENCRYPTION_KEY", raising=False)
    with pytest.raises(MissingEncryptionKeyError):
        credentials.encrypt_value("x")
