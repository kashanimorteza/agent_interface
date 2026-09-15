from __future__ import annotations

import pytest

from database.credentials import (
    apply_at_rest_treatment,
    decrypt_credential,
    encrypt_credential,
    hash_credential,
    verify_hashed_credential,
)
from database.exceptions import UnsupportedCredentialModeError


def test_hash_is_one_way_and_verifiable() -> None:
    stored = hash_credential("correct horse battery staple")
    assert "correct horse battery staple" not in stored
    assert verify_hashed_credential("correct horse battery staple", stored)
    assert not verify_hashed_credential("wrong password", stored)


def test_encryption_is_reversible_only_with_the_key() -> None:
    stored = encrypt_credential("s3cr3t-api-key")
    assert "s3cr3t-api-key" not in stored
    assert decrypt_credential(stored) == "s3cr3t-api-key"


def test_unsupported_mode_is_rejected() -> None:
    with pytest.raises(UnsupportedCredentialModeError):
        apply_at_rest_treatment("plaintext", "x")
    with pytest.raises(UnsupportedCredentialModeError):
        apply_at_rest_treatment("unknown-mode", "x")
