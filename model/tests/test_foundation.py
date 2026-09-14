import pytest
from pydantic import SecretStr, ValidationError

from model import Broker, User


def test_unknown_field_rejected_consistently():
    with pytest.raises(ValidationError):
        User.model_validate(
            {
                "name": "A",
                "username": "a",
                "password": "p",
                "api_key": "k",
                "unexpected": "x",
            }
        )
    with pytest.raises(ValidationError):
        Broker.model_validate({"name": "B", "user_id": 1, "unexpected": "x"})


def test_missing_optional_field_resolves_to_declared_default_consistently():
    user = User(name="A", username="a", password=SecretStr("p"), api_key=SecretStr("k"))
    broker = Broker(name="B", user_id=1)
    assert user.is_active is True
    assert user.description is None
    assert broker.is_active is True
    assert broker.description is None


def test_validation_is_deterministic():
    data = {"name": "B", "user_id": 1}
    first = Broker(**data)
    second = Broker(**data)
    assert first.model_dump() == second.model_dump()


def test_shared_unique_together_mechanism_is_per_definition():
    assert User.unique_together == (("name",),)
    assert Broker.unique_together == (("user_id", "name"),)
    assert User.unique_together != Broker.unique_together
