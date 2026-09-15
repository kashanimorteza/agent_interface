"""Verifies P2T1: the Storage Adapter and Instance Registry."""

from __future__ import annotations

import pytest

from database.adapter import (
    UnknownInstanceError,
    default_instance_key,
    get_engine,
    instance_registry,
)


def test_registry_lists_configured_instances_with_default() -> None:
    registry = instance_registry()
    keys = {entry["key"] for entry in registry}
    assert "general" in keys
    defaults = [entry for entry in registry if entry["is_default"]]
    assert len(defaults) == 1
    assert defaults[0]["key"] == default_instance_key()


def test_registry_exposes_no_connection_or_secret_value() -> None:
    for entry in instance_registry():
        for value in entry.values():
            assert not hasattr(value, "connect")
            assert "secret" not in str(value).lower()
            assert "password" not in str(value).lower()


def test_default_instance_opens_a_working_connection(fresh_db: None) -> None:
    engine = get_engine()
    with engine.connect() as connection:
        assert connection.exec_driver_sql("select 1").scalar() == 1


def test_unknown_instance_is_rejected() -> None:
    with pytest.raises(UnknownInstanceError):
        get_engine("does-not-exist")
