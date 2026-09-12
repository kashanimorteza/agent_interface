"""Public interface import check."""

import my_database
from my_database import operations as operations_module


def test_canonical_module_qualified_import() -> None:
    assert my_database.operations.add is my_database.add


def test_alternate_explicit_module_import() -> None:
    assert operations_module.add is my_database.add


def test_every_declared_public_name_is_reachable() -> None:
    for name in my_database.__all__:
        assert hasattr(my_database, name), f"declared public name {name!r} is not reachable"


def test_import_performs_no_io() -> None:
    assert my_database.instance_registry is not None
