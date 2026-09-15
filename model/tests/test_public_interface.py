"""Verifies that every Domain Definition is reachable through Model's Public Interface."""

import model

EXPECTED_DOMAIN_DEFINITIONS = {
    "User",
    "TradingPlatform",
    "Instance",
    "Currency",
    "Broker",
    "Asset",
    "AccountGroup",
    "Account",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
}


def test_public_interface_exposes_every_domain_definition():
    exported = set(model.__all__)
    assert EXPECTED_DOMAIN_DEFINITIONS <= exported


def test_every_exported_domain_definition_is_a_domain_model():
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        cls = getattr(model, name)
        assert issubclass(cls, model.DomainModel)


def test_foundation_types_are_exported():
    assert model.DomainModel is not None
    assert model.ForeignKey is not None
    assert model.Credential is not None
