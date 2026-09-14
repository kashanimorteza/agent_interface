"""Verifies the Database component README (task P2-G12-T1)."""

from __future__ import annotations

import re
from pathlib import Path

import model

import database

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


def test_documented_imports_match_database_all_exactly() -> None:
    match = re.search(r"from database import \(\s*(.*?)\s*\)", README, re.DOTALL)
    assert match is not None
    documented = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert documented == set(database.__all__)


def test_documented_usage_example_runs(db) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    fetched = db.get(model.User, user.id)
    assert fetched is not None
    assert fetched.password == "***protected***"

    with db.transaction() as txn:
        db.create(model.TradingPlatform(name="MetaTrader 5", code="metatrader_5"), txn=txn)
        db.create(model.TradingPlatform(name="Binance", code="binance"), txn=txn)

    infos = db.instances.list_instances()
    assert infos

    result = db.execute_command("count_positions_by_execution", user_id=user.id)
    assert result is not None

    database.seed_initial_data(db)
    admins = db.list(model.User, name="Admin")
    assert len(admins) == 1


def test_documented_commands_match_the_real_ones() -> None:
    for command in (
        "alembic upgrade head",
        "uv run pytest",
        "uv run ruff check .",
        "uv run pyright",
    ):
        assert command in README


def test_secret_scan_clean() -> None:
    forbidden_patterns = [
        r"api_key\s*=\s*['\"](?!key\b)[A-Za-z0-9]{8,}['\"]",
        r"password\s*=\s*['\"](?!pw\b)[A-Za-z0-9]{8,}['\"]",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, README), (
            f"README appears to contain a usable secret: {pattern}"
        )
