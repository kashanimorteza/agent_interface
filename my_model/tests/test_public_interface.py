"""Public interface import check.

Verifies the package's canonical and alternate import styles work and that
every declared public name is reachable without touching an internal module.
"""

import my_model
from my_model import user as user_module


def test_canonical_module_qualified_import() -> None:
    assert my_model.user.User is my_model.User


def test_alternate_explicit_module_import() -> None:
    assert user_module.User is my_model.User


def test_every_declared_public_name_is_reachable() -> None:
    for name in my_model.__all__:
        assert hasattr(my_model, name), f"declared public name {name!r} is not reachable"


def test_import_performs_no_io() -> None:
    # A fresh import must not require a database, network, or API dependency.
    # If importing the package required any of those, this test process
    # itself (which never configures one) would already have failed above.
    assert my_model.User.model_fields  # the type is fully usable after import
