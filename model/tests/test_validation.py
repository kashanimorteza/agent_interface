"""Verifies deterministic, strict validation behavior of every Domain Definition."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from model import User


def test_valid_domain_definitions_construct_successfully(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, data = domain_sample
    instance = domain_cls(**data)
    for field_name, value in data.items():
        assert getattr(instance, field_name) == value


def test_missing_required_field_is_rejected(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, data = domain_sample
    incomplete = dict(data)
    # `id` is required (no default) on every Domain Definition.
    del incomplete["id"]
    with pytest.raises(ValidationError):
        domain_cls(**incomplete)


def test_undeclared_field_is_rejected(
    domain_sample: tuple[type, dict[str, object]],
) -> None:
    domain_cls, data = domain_sample
    with pytest.raises(ValidationError):
        domain_cls(**data, undeclared_field="not part of the Domain Definition")


def test_strict_mode_rejects_implicit_type_coercion() -> None:
    with pytest.raises(ValidationError):
        User(
            id="1",  # pyright: ignore[reportArgumentType]  # an int Field must not silently coerce a string
            name="Admin",
            username="admin",
            password="secret",
            api_key="key",
            is_active=True,
            description=None,
        )


def test_nullable_field_accepts_none() -> None:
    user = User(
        id=1,
        name="Admin",
        username="admin",
        password="secret",
        api_key="key",
        is_active=True,
        description=None,
    )
    assert user.description is None


def test_default_is_applied_when_field_is_omitted() -> None:
    user = User(id=1, name="Admin", username="admin", password="secret", api_key="key")
    assert user.is_active is True
    assert user.description is None
