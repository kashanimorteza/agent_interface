"""Public interface import check."""

import my_backend


def test_app_is_importable_and_configured() -> None:
    assert my_backend.app.title == "Trading Assistant Backend"


def test_every_declared_public_name_is_reachable() -> None:
    for name in my_backend.__all__:
        assert hasattr(my_backend, name)
