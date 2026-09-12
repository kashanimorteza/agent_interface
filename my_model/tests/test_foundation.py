import pytest
from pydantic import ValidationError

from my_model._base import BaseModel


def test_package_imports() -> None:
    import my_model  # noqa: F401


def test_base_model_accepts_valid_instance_and_rejects_unexpected_field() -> None:
    class Sample(BaseModel):
        value: int

    assert Sample(value=1).value == 1

    with pytest.raises(ValidationError):
        Sample(value=1, unexpected="not allowed")  # type: ignore[call-arg]


def test_base_class_is_not_named_model() -> None:
    from my_model import _base

    assert not hasattr(_base, "Model")
    assert _base.BaseModel.__name__ == "BaseModel"
