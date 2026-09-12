"""Instance discovery and selection."""

import pytest

import my_database


def test_registry_lists_configured_instances_and_default() -> None:
    identities = my_database.instance_registry.list()
    keys = {identity.key for identity in identities}
    assert "general" in keys
    assert my_database.instance_registry.default.key == "general"


def test_omitted_selection_uses_the_default() -> None:
    resolved = my_database.instance_registry.resolve(None)
    assert resolved.key == my_database.instance_registry.default.key


def test_explicit_unknown_instance_is_rejected_not_redirected() -> None:
    with pytest.raises(my_database.errors.UnknownInstanceError):
        my_database.instance_registry.resolve("does-not-exist")


def test_registry_exposes_no_connection_or_secret() -> None:
    for identity in my_database.instance_registry.list():
        assert not hasattr(identity, "connection")
        assert not hasattr(identity, "password")
        assert not hasattr(identity, "secret")
