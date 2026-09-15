"""Verifies P2T3: declared credential at-rest treatment."""

from __future__ import annotations

import pytest

from database.credentials import (
    UnsupportedCredentialTreatmentError,
    apply_treatment,
    decrypt_value,
    encrypt_value,
    hash_value,
    verify_hash,
)


def test_hash_treatment_is_one_way_but_verifiable() -> None:
    stored = hash_value("s3cret")
    assert stored != "s3cret"
    assert verify_hash("s3cret", stored) is True
    assert verify_hash("wrong", stored) is False


def test_encrypted_treatment_is_reversible_and_protected() -> None:
    token = encrypt_value("api-key-value")
    assert token != "api-key-value"
    assert decrypt_value(token) == "api-key-value"


def test_apply_treatment_dispatches_by_classification() -> None:
    hashed = apply_treatment("hash", "value")
    assert verify_hash("value", hashed)
    encrypted = apply_treatment("encrypted", "value")
    assert decrypt_value(encrypted) == "value"


def test_missing_or_unsupported_classification_is_rejected() -> None:
    with pytest.raises(UnsupportedCredentialTreatmentError):
        apply_treatment(None, "value")
    with pytest.raises(UnsupportedCredentialTreatmentError):
        apply_treatment("plaintext", "value")
