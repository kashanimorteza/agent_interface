import model


def test_every_domain_definition_is_reachable_by_one_public_identity():
    names = [
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
    ]
    for name in names:
        assert hasattr(model, name), (
            f"{name} is not reachable from model's Public Interface"
        )
        assert name in model.__all__
