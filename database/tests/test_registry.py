"""Tests for the Database Instance Registry (task P2-G2-T1)."""

from __future__ import annotations

import dataclasses

import pytest

from database.exceptions import UnknownDatabaseInstance
from database.registry import InstanceRegistry
from database.runtime_config import RuntimeConfig


def test_registry_lists_every_configured_instance_and_the_correct_default(
    test_config: RuntimeConfig,
) -> None:
    registry = InstanceRegistry(test_config)
    listed = registry.list_instances()
    assert {info.key for info in listed} == set(test_config.instances)
    defaults = [info for info in listed if info.is_default]
    assert [d.key for d in defaults] == [test_config.default_instance]


def test_registry_rejects_unknown_instance(test_config: RuntimeConfig) -> None:
    registry = InstanceRegistry(test_config)
    with pytest.raises(UnknownDatabaseInstance):
        registry.get("does-not-exist")


def test_registry_exposes_no_connection_or_secret(test_config: RuntimeConfig) -> None:
    registry = InstanceRegistry(test_config)
    for info in registry.list_instances():
        dumped = dataclasses.asdict(info)
        for value in dumped.values():
            text = str(value).lower()
            assert "sqlite:" not in text
            assert "password" not in text
            assert "secret" not in text
