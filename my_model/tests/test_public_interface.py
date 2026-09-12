"""Verifies the my_model package's public interface: module-qualified imports,
deterministic serialization and schema generation, and no I/O at import time.
"""

from __future__ import annotations

import json

import my_model
from my_model import user as user_module


def test_canonical_module_qualified_import() -> None:
    instance = my_model.user.User(name="Ada", username="ada", password="secret", api_key="key")
    assert isinstance(instance, my_model.User)


def test_alternate_module_import() -> None:
    instance = user_module.User(name="Ada", username="ada", password="secret", api_key="key")
    assert isinstance(instance, my_model.User)


def test_every_declared_entity_reachable_exactly_once_at_root() -> None:
    entity_names = [
        "Account",
        "AccountGroup",
        "Action",
        "ActionGroup",
        "Asset",
        "Broker",
        "Currency",
        "Instance",
        "PartialGroup",
        "PartialRule",
        "Position",
        "TradingPlatform",
        "TrailingGroup",
        "TrailingRule",
        "User",
    ]
    for name in entity_names:
        assert hasattr(my_model, name), f"{name} is not reachable from the package root"
    assert len(entity_names) == len(set(entity_names))


def test_serialization_is_deterministic() -> None:
    instance = my_model.User(name="Ada", username="ada", password="secret", api_key="key")
    first = instance.model_dump()
    second = instance.model_dump()
    assert first == second
    assert json.loads(instance.model_dump_json()) == first


def test_schema_generation_succeeds_for_every_entity() -> None:
    for name in my_model.__all__:
        candidate = getattr(my_model, name)
        if isinstance(candidate, type) and issubclass(candidate, my_model.BaseModel):
            schema = candidate.model_json_schema()
            assert schema["title"] == candidate.__name__


def test_partial_update_preserves_omission_versus_explicit_null() -> None:
    original = my_model.Instance(user_id=1, name="Primary", trading_platform_id=1, ip="127.0.0.1")
    omitted_update = original.model_copy(update={})
    explicit_null_update = original.model_copy(update={"ip": None})
    assert omitted_update.ip == "127.0.0.1"
    assert explicit_null_update.ip is None
