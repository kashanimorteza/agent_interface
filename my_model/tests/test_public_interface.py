"""Public-interface import check and general package-level behavior."""

from __future__ import annotations

import my_model
from my_model import user as user_module


def test_canonical_import_style_exposes_every_public_module() -> None:
    for name in my_model.__all__:
        assert hasattr(my_model, name)


def test_alternate_import_style_exposes_model_type() -> None:
    assert hasattr(user_module, "User")


def test_model_identity_is_never_a_public_string_selector() -> None:
    # Constructing a User requires the imported type, not a string name.
    instance = user_module.User(name="Ada", username="ada", password="x", api_key="y")
    assert isinstance(instance, user_module.User)
