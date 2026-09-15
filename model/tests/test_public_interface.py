"""Verifies every Domain Definition is reachable through Model's Public Interface."""

from __future__ import annotations

import model
from model import ModelBase

EXPECTED_DOMAIN_DEFINITIONS = {
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
}


def test_every_domain_definition_is_publicly_exported() -> None:
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        assert hasattr(model, name), (
            f"{name} is not reachable through model's Public Interface"
        )


def test_every_public_domain_definition_is_a_model_base_subclass() -> None:
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        cls = getattr(model, name)
        assert issubclass(cls, ModelBase)


def test_public_interface_has_no_undeclared_domain_definitions() -> None:
    exported_classes = {
        name
        for name in model.__all__
        if isinstance(getattr(model, name), type)
        and issubclass(getattr(model, name), ModelBase)
        and getattr(model, name) is not ModelBase
    }
    assert exported_classes == EXPECTED_DOMAIN_DEFINITIONS
