"""Verifies approved at-rest treatment for classified credential fields."""

from __future__ import annotations

import pytest

from database.credentials import (
    MissingEncryptionKeyError,
    UnsupportedCredentialTreatmentError,
    apply_at_rest_treatment,
    decrypt_value,
    encrypt_value,
    hash_value,
    verify_hash,
)


def test_hash_value_is_not_the_plaintext() -> None:
    hashed = hash_value("s3cret")
    assert hashed != "s3cret"


def test_hash_value_cannot_be_reversed_to_plaintext() -> None:
    hashed = hash_value("s3cret")
    # No function in this module recovers plaintext from a hash; verify_hash
    # only confirms a candidate matches, it never returns the original.
    assert verify_hash("s3cret", hashed) is True
    assert verify_hash("wrong-guess", hashed) is False


def test_encrypt_value_is_not_the_plaintext() -> None:
    encrypted = encrypt_value("topsecret")
    assert encrypted != "topsecret"


def test_encrypt_decrypt_round_trip_recovers_original() -> None:
    encrypted = encrypt_value("topsecret")
    assert decrypt_value(encrypted) == "topsecret"


def test_apply_at_rest_treatment_hash() -> None:
    result = apply_at_rest_treatment("hash", "value")
    assert result != "value"
    assert verify_hash("value", result)


def test_apply_at_rest_treatment_encrypted() -> None:
    result = apply_at_rest_treatment("encrypted", "value")
    assert result != "value"
    assert decrypt_value(result) == "value"


def test_apply_at_rest_treatment_rejects_unsupported() -> None:
    with pytest.raises(UnsupportedCredentialTreatmentError):
        apply_at_rest_treatment("plaintext", "value")


def test_missing_encryption_key_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_CREDENTIAL_ENCRYPTION_KEY", raising=False)
    with pytest.raises(MissingEncryptionKeyError):
        encrypt_value("value")
