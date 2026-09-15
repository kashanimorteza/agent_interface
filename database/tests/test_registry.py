"""Verifies the public Instance Registry."""

from __future__ import annotations

import dataclasses

from database.adapter import StorageAdapter
from database.registry import InstanceDescriptor, InstanceRegistry


def test_registry_lists_every_configured_instance(adapter: StorageAdapter) -> None:
    registry = InstanceRegistry(adapter)
    keys = {i.key for i in registry.list_instances()}
    assert keys == {i.key for i in adapter.instances()}


def test_registry_default_matches_adapter_default(adapter: StorageAdapter) -> None:
    registry = InstanceRegistry(adapter)
    assert registry.default.key == adapter.default_instance_key


def test_instance_descriptor_exposes_no_connection_or_secret() -> None:
    fields = {f.name for f in dataclasses.fields(InstanceDescriptor)}
    assert fields == {"key", "name", "purpose"}
