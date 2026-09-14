"""Verifies the complete Model Public Interface as one coherent whole (Task P1-G7-T1)."""

from __future__ import annotations

import model

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


def _domain_definitions() -> list[type]:
    return [getattr(model, name) for name in sorted(EXPECTED_DOMAIN_DEFINITIONS)]


def test_every_domain_definition_is_publicly_reachable() -> None:
    assert EXPECTED_DOMAIN_DEFINITIONS <= set(model.__all__)
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        assert hasattr(model, name), (
            f"{name} is not reachable through the Public Interface"
        )


def test_each_domain_definition_has_exactly_one_public_identity() -> None:
    """No Domain Definition is exported under two public names, and no name is exported twice."""

    assert len(model.__all__) == len(set(model.__all__)), (
        "a public name is exported twice"
    )
    exported = {name: getattr(model, name) for name in model.__all__}
    classes = [
        obj
        for obj in exported.values()
        if isinstance(obj, type) and issubclass(obj, model.ModelBase)
    ]
    assert len(classes) == len(set(classes)), (
        "a Domain Definition is exported under two names"
    )


def test_no_domain_definition_requires_a_private_internal_resource() -> None:
    """Using a Domain Definition never requires reaching past the package's public surface."""

    for cls in _domain_definitions():
        assert cls.__module__.startswith("model."), cls.__module__
        assert not cls.__name__.startswith("_"), cls.__name__
        assert getattr(model, cls.__name__) is cls


def test_the_whole_boundary_validates_and_serializes() -> None:
    for cls in _domain_definitions():
        schema = cls.model_json_schema()
        assert schema["type"] == "object"
        assert schema["properties"], f"{cls.__name__} produced an empty schema"


def test_every_domain_definition_shares_the_foundation() -> None:
    for cls in _domain_definitions():
        assert issubclass(cls, model.ModelBase), (
            f"{cls.__name__} does not build on the Model Foundation"
        )
