"""Verifies the Storage Adapter's Instance resolution and connection behavior."""

from __future__ import annotations

import pytest

from database.adapter import StorageAdapter, UnknownInstanceError


def test_omitted_selection_resolves_to_default(adapter: StorageAdapter) -> None:
    resolved = adapter.resolve_instance(None)
    assert resolved.key == adapter.default_instance_key


def test_explicit_known_instance_resolves(adapter: StorageAdapter) -> None:
    resolved = adapter.resolve_instance("general")
    assert resolved.key == "general"


def test_explicit_unknown_instance_is_rejected(adapter: StorageAdapter) -> None:
    with pytest.raises(UnknownInstanceError):
        adapter.resolve_instance("does-not-exist")


def test_connect_yields_a_usable_connection(adapter: StorageAdapter) -> None:
    from sqlalchemy import text

    with adapter.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()
    assert result == 1
