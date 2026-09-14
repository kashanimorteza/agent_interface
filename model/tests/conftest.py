"""Shared helpers for verifying Domain Definitions against the Target."""

from __future__ import annotations

from typing import Any


def assert_exact_fields(model_cls: Any, expected: dict[str, bool]) -> None:
    """Assert model_cls declares exactly `expected`'s fields, each with the given required-ness."""

    fields = model_cls.model_fields
    assert set(fields) == set(expected), (
        f"{model_cls.__name__} fields {sorted(fields)} "
        f"do not match Target-stated fields {sorted(expected)}"
    )
    for name, required in expected.items():
        actual = fields[name].is_required()
        assert actual == required, (
            f"{model_cls.__name__}.{name} required={actual}, expected {required}"
        )


def assert_unique_constraints(
    model_cls: Any, expected: tuple[tuple[str, ...], ...]
) -> None:
    """Assert model_cls declares exactly the uniqueness the Target states for it."""

    actual = model_cls.unique_constraints
    assert set(actual) == set(expected), (
        f"{model_cls.__name__} declares uniqueness {actual}, "
        f"but the Target states {expected}"
    )
    for group in actual:
        for field in group:
            assert field in model_cls.model_fields, (
                f"{model_cls.__name__} declares uniqueness over unknown field {field!r}"
            )


def assert_credential_fields(model_cls: Any, names: tuple[str, ...]) -> None:
    """Assert exactly `names` carry credential meaning on model_cls."""

    actual = {
        name
        for name, field in model_cls.model_fields.items()
        if isinstance(field.json_schema_extra, dict)
        and field.json_schema_extra.get("credential")
    }
    assert actual == set(names), (
        f"{model_cls.__name__} credential fields {sorted(actual)} "
        f"do not match the Target's credential meaning {sorted(names)}"
    )
