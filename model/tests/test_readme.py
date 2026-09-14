"""Verifies the Model component README (Task P1-G8-T1)."""

from __future__ import annotations

import pathlib
import re

import model

README = pathlib.Path(__file__).resolve().parent.parent / "README.md"
TEXT = README.read_text(encoding="utf-8")


def test_readme_exists_and_covers_the_required_topics() -> None:
    for heading in (
        "Public surface",
        "Structure",
        "Setup",
        "Use",
        "Verification",
        "Troubleshooting",
    ):
        assert f"## {heading}" in TEXT, f"README is missing the {heading} section"


def test_documented_public_surface_matches_the_actual_public_surface() -> None:
    block = re.search(r"```python\nfrom model import \(\n(.*?)\)\n```", TEXT, re.DOTALL)
    assert block, "README does not document the public surface as an importable block"
    documented = {
        line.strip().rstrip(",") for line in block.group(1).splitlines() if line.strip()
    }
    assert documented == set(model.__all__), (
        f"README documents {sorted(documented)} but the package exports {sorted(model.__all__)}"
    )


def test_documented_usage_example_runs() -> None:
    admin = model.User(
        id=1, name="Admin", username="admin", password="<password>", api_key="<api-key>"
    )
    assert admin.model_dump()["name"] == "Admin"
    assert model.User.model_validate_json(admin.model_dump_json()) == admin
    assert model.User.model_json_schema()["type"] == "object"
    assert model.User.unique_constraints == (("name",),)
    assert model.Account.unique_constraints == (
        ("name",),
        ("group_id", "broker_id", "instance_id"),
    )


def test_documented_verification_commands_are_the_real_ones() -> None:
    for command in (
        "uv sync",
        "uv run pytest",
        "uv run ruff check .",
        "uv run pyright",
    ):
        assert command in TEXT, f"README does not document `{command}`"


def test_readme_exposes_no_usable_secret() -> None:
    """Placeholders are fine; anything resembling a real key, token, or private key is not."""

    private_key = "-----BEGIN"
    assert private_key not in TEXT, "README contains a private key block"

    code_values = re.findall(
        r"""(?:password|api_key|token|secret)\s*=\s*["']([^"']*)["']""", TEXT
    )
    for value in code_values:
        assert value.startswith("<") and value.endswith(">"), (
            f"README assigns a non-placeholder credential value: {value!r}"
        )

    for candidate in re.findall(r"[A-Za-z0-9_\-]{24,}", TEXT):
        assert not re.fullmatch(r"[A-Fa-f0-9]{24,}", candidate), (
            f"README contains a hex string that looks like a real token: {candidate!r}"
        )
