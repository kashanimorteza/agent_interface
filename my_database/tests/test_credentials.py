from __future__ import annotations

import pytest
from cryptography.fernet import Fernet

from my_database._credentials import (
    decrypt_value,
    encrypt_value,
    hash_value,
    verify_hash,
)


def test_hash_value_is_one_way_and_verifiable():
    stored = hash_value("correct horse battery staple")
    assert stored != "correct horse battery staple"
    assert verify_hash("correct horse battery staple", stored) is True
    assert verify_hash("wrong password", stored) is False


def test_hash_value_uses_a_fresh_salt_each_time():
    a = hash_value("same-input")
    b = hash_value("same-input")
    assert a != b  # different salts -> different stored strings
    assert verify_hash("same-input", a) is True
    assert verify_hash("same-input", b) is True


def test_encrypt_decrypt_round_trip():
    key = Fernet.generate_key()
    token = encrypt_value("api-secret", key)
    assert token != "api-secret"
    assert decrypt_value(token, key) == "api-secret"


def test_decrypt_with_wrong_key_is_rejected():
    key = Fernet.generate_key()
    other_key = Fernet.generate_key()
    token = encrypt_value("api-secret", key)
    with pytest.raises(ValueError):
        decrypt_value(token, other_key)
