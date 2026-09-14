"""Verifies the complete Model Public Interface as one whole (task P1-G7-T1)."""

from __future__ import annotations

import model

_DOMAIN_DEFINITIONS = [
    model.User,
    model.TradingPlatform,
    model.Instance,
    model.Currency,
    model.Broker,
    model.Asset,
    model.AccountGroup,
    model.Account,
    model.TrailingGroup,
    model.TrailingRule,
    model.PartialGroup,
    model.PartialRule,
    model.ActionGroup,
    model.Action,
    model.Position,
]


def test_every_domain_definition_reachable_through_public_interface() -> None:
    for cls in _DOMAIN_DEFINITIONS:
        assert getattr(model, cls.__name__) is cls
        assert cls.__name__ in model.__all__


def test_no_duplicate_public_identity() -> None:
    names = [cls.__name__ for cls in _DOMAIN_DEFINITIONS]
    assert len(names) == len(set(names)) == 15


def test_no_private_resource_dependency() -> None:
    for cls in _DOMAIN_DEFINITIONS:
        module_path = cls.__module__
        assert not any(part.startswith("_") for part in module_path.split("."))


def test_schema_generation_non_empty_for_all() -> None:
    for cls in _DOMAIN_DEFINITIONS:
        schema = cls.model_json_schema()
        assert schema["properties"]


def test_all_build_on_the_foundation() -> None:
    for cls in _DOMAIN_DEFINITIONS:
        assert issubclass(cls, model.ModelBase)
