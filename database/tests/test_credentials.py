"""Tests for credential at-rest protection resolution (supports task P2-G3-T1..T3, P2-G5-T2)."""

from __future__ import annotations

from database.credentials import (
    decrypt_value,
    encrypt_value,
    hash_value,
    resolve_mode,
    verify_hash,
)


def test_resolve_mode_uses_explicit_target_overrides() -> None:
    assert resolve_mode("User", "password") == "hash"
    assert resolve_mode("User", "api_key") == "hash"
    assert resolve_mode("Instance", "password") == "encrypted"
    assert resolve_mode("Instance", "api_key") == "encrypted"
    assert resolve_mode("Account", "password") == "encrypted"


def test_resolve_mode_falls_back_to_field_default_when_no_explicit_override() -> None:
    assert resolve_mode("SomeFutureModel", "password") == "hash"
    assert resolve_mode("SomeFutureModel", "api_key") == "encrypted"


def test_hash_is_one_way_and_verifiable() -> None:
    stored = hash_value("correct horse battery staple")
    assert stored != "correct horse battery staple"
    assert verify_hash("correct horse battery staple", stored)
    assert not verify_hash("wrong password", stored)


def test_encryption_is_reversible_only_with_the_resolved_key() -> None:
    token = encrypt_value("super-secret-value", instance="general")
    assert token != "super-secret-value"
    assert decrypt_value(token, instance="general") == "super-secret-value"
