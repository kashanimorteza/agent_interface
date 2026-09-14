"""Verifies the Model component README (task P1-G8-T1)."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import ValidationError

import model
from model import User

README = (Path(__file__).parent.parent / "README.md").read_text(encoding="utf-8")

_REQUIRED_SECTIONS = [
    "## Public surface",
    "## Setup",
    "## Installation",
    "## Configuration",
    "## Use",
    "## Verification",
    "## Troubleshooting",
]


def test_required_sections_present() -> None:
    for section in _REQUIRED_SECTIONS:
        assert section in README, f"README is missing the {section!r} section"


def test_documented_imports_match_model_all_exactly() -> None:
    match = re.search(r"from model import \(\s*(.*?)\s*\)", README, re.DOTALL)
    assert match is not None
    documented = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert documented == set(model.__all__)


def test_documented_usage_example_runs() -> None:
    admin = User(name="Admin", username="admin", password="change-me", api_key="generated-key")
    assert admin.is_active is True
    assert admin.id is None
    restored = User.model_validate_json(admin.model_dump_json())
    assert restored == admin
    assert User.UNIQUE_CONSTRAINTS == (("name",),)
    assert User.model_fields["password"].json_schema_extra == {"credential": True}

    invalid_kwargs = {
        "name": "Admin",
        "username": "admin",
        "password": "x",
        "api_key": "y",
        "extra_field": "nope",
    }
    try:
        User(**invalid_kwargs)  # pyright: ignore[reportArgumentType]
    except ValidationError:
        pass
    else:
        raise AssertionError("expected a ValidationError for the extra field")


def test_documented_commands_match_the_real_ones() -> None:
    for command in ("uv sync", "uv run pytest", "uv run ruff check .", "uv run pyright"):
        assert command in README


def test_secret_scan_clean() -> None:
    forbidden_patterns = [
        r"api_key\s*=\s*['\"](?!generated-key)[A-Za-z0-9]{8,}['\"]",
        r"password\s*=\s*['\"](?!change-me|x)[A-Za-z0-9]{8,}['\"]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, README), (
            f"README appears to contain a usable secret: {pattern}"
        )
