"""The public Instance Registry (Task P2-T1)."""

from __future__ import annotations

import my_database as db


def test_registry_lists_configured_instances_without_secrets():
    instances = db.registry.list_instances()
    keys = {i.key for i in instances}
    assert "general" in keys
    for instance in instances:
        assert not hasattr(instance, "connection")
        assert not hasattr(instance, "password")


def test_default_instance_is_general():
    default = db.registry.default_instance()
    assert default.key == "general"
