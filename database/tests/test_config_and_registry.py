from __future__ import annotations

import pytest

from database.config import load_storage_config
from database.exceptions import DatabaseConfigurationError, UnknownInstanceError
from database.registry import instance_registry


def test_runtime_configuration_resolves_engine_and_default() -> None:
    cfg = load_storage_config()
    assert cfg.default_instance == "general"
    assert cfg.instances["general"].engine == "sqlite"
    path = cfg.storage_path()
    assert path.name == "trading_assistant_general.db"


def test_invalid_engine_reference_is_rejected(tmp_path) -> None:
    bad = tmp_path / "database.yaml"
    bad.write_text(
        "engines:\n  sqlite: {}\ninstances:\n  general:\n    name: G\n"
        "    purpose: P\n    engine: postgres\n    database: x\n"
        "default_instance: general\n"
    )
    with pytest.raises(DatabaseConfigurationError):
        load_storage_config(bad)


def test_instance_registry_lists_default_and_rejects_unknown() -> None:
    registry = instance_registry()
    assert registry.default == "general"
    keys = {i.key for i in registry.instances}
    assert "general" in keys

    default_identity = registry.get()
    assert default_identity.key == "general"

    with pytest.raises(UnknownInstanceError):
        registry.get("does-not-exist")


def test_registry_never_exposes_connection_or_secret() -> None:
    registry = instance_registry()
    for identity in registry.instances:
        assert not hasattr(identity, "connection")
        assert not hasattr(identity, "secret")
        assert not hasattr(identity, "password")
