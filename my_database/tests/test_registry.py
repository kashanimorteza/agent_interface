from __future__ import annotations

from my_database import registry


def test_list_instances_exposes_only_identity_fields():
    identities = registry.list_instances()
    assert len(identities) == 1
    identity = identities[0]
    assert identity.key == "general"
    assert identity.name
    assert identity.purpose
    assert not hasattr(identity, "connection")
    assert not hasattr(identity, "engine")


def test_default_instance_matches_configured_default():
    identity = registry.default_instance()
    assert identity.key == "general"
