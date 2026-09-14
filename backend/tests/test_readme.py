"""Verifies the Backend component README (task P3-G14-T1)."""

from __future__ import annotations

import re
from pathlib import Path

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


def test_readme_documents_delete_and_search() -> None:
    assert "DELETE /{resource}/{id}" in README
    assert "GET /{resource}/search" in README


def test_documented_endpoints_match_the_real_ones(client, auth_headers) -> None:
    schema = client.get("/openapi.json").json()
    assert "/v1/trading-platform" in schema["paths"]
    assert "/health" in schema["paths"]
    assert "/ready" in schema["paths"]


def test_documented_configuration_variables_match_the_real_settings() -> None:
    from backend.config import Settings

    documented = {
        "cors_allowed_origins",
        "host",
        "port",
        "api_version",
        "database_instance",
        "request_timeout_seconds",
        "max_retry_attempts",
        "shutdown_timeout_seconds",
    }
    assert documented == set(Settings.model_fields)


def test_documented_commands_match_the_real_ones() -> None:
    for command in (
        "uv run pytest",
        "uv run ruff check .",
        "uv run pyright",
        "fastapi run",
        "uv run alembic upgrade head",
    ):
        assert command in README


def test_secret_scan_clean() -> None:
    forbidden_patterns = [
        r"api_key\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]",
        r"password\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, README), (
            f"README appears to contain a usable secret: {pattern}"
        )
