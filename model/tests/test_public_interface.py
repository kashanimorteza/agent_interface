"""Package-level verification: every Domain Definition is reachable through
one Public Interface with an unambiguous identity."""

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


def test_every_domain_definition_is_publicly_reachable():
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        assert hasattr(model, name), (
            f"{name} is not exposed by the Model Public Interface"
        )
        assert name in model.__all__


def test_every_domain_definition_has_one_unambiguous_identity():
    seen = {}
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        obj = getattr(model, name)
        assert obj not in seen.values(), f"{name} duplicates another public identity"
        seen[name] = obj


def test_every_domain_definition_is_a_domain_model():
    for name in EXPECTED_DOMAIN_DEFINITIONS:
        obj = getattr(model, name)
        assert issubclass(obj, model.DomainModel)
