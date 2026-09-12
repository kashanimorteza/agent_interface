import types

import my_model

EXPECTED_MODELS = {
    "account": "Account",
    "account_group": "AccountGroup",
    "action": "Action",
    "action_group": "ActionGroup",
    "asset": "Asset",
    "broker": "Broker",
    "currency": "Currency",
    "instance": "Instance",
    "partial_group": "PartialGroup",
    "partial_rule": "PartialRule",
    "position": "Position",
    "trading_platform": "TradingPlatform",
    "trailing_group": "TrailingGroup",
    "trailing_rule": "TrailingRule",
    "user": "User",
}


def test_every_model_reachable_through_canonical_module_qualified_interface() -> None:
    for module_name, class_name in EXPECTED_MODELS.items():
        submodule = getattr(my_model, module_name)
        assert isinstance(submodule, types.ModuleType), (
            f"my_model.{module_name} is not reachable as a module after `import my_model`"
        )
        model_type = getattr(submodule, class_name)
        assert isinstance(model_type, type)


def test_canonical_interface_reachable_via_from_import_too() -> None:
    from my_model import user

    assert user.User is my_model.User


def test_each_model_exposed_exactly_once_through_canonical_interface() -> None:
    seen_types = set()
    for module_name, class_name in EXPECTED_MODELS.items():
        submodule = getattr(my_model, module_name)
        model_type = getattr(submodule, class_name)
        assert model_type not in seen_types, f"{class_name} is exposed by more than one submodule"
        seen_types.add(model_type)
    assert len(seen_types) == len(EXPECTED_MODELS)


def test_model_identity_is_never_a_string_registry_lookup() -> None:
    assert not hasattr(my_model, "MODELS")
    assert not hasattr(my_model, "get_model")
    assert not hasattr(my_model, "registry")


def test_flat_convenience_reexports_match_canonical_modules() -> None:
    for module_name, class_name in EXPECTED_MODELS.items():
        submodule = getattr(my_model, module_name)
        assert getattr(my_model, class_name) is getattr(submodule, class_name)


def test_types_module_is_reachable_and_exports_percentage() -> None:
    assert hasattr(my_model.types, "Percentage")
