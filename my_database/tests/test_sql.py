"""The controlled parameterized SQL execution route (Task P2-T9)."""

from __future__ import annotations

import pytest

import my_database as db
from my_database.exceptions import UnsupportedOperation


def test_select_result_redacts_credential_columns():
    rows = db.sql.execute(
        "select id, name, password, api_key from users where name = :name",
        {"name": "Admin"},
        instance="general",
    )
    assert rows[0]["password"] == "••••••••"
    assert rows[0]["api_key"] == "••••••••"


@pytest.mark.parametrize(
    "statement",
    [
        "DROP TABLE users",
        "ALTER TABLE users ADD COLUMN x TEXT",
        "select * from users; select * from users",
        "select * from unknown_table",
        "GRANT ALL ON users TO nobody",
        "PRAGMA table_info(users)",
        "VACUUM",
    ],
)
def test_rejects_structural_privilege_and_unknown_table_statements(statement):
    with pytest.raises(UnsupportedOperation):
        db.sql.execute(statement, instance="general")


def test_parameterized_write_applies_and_is_observable():
    db.sql.execute(
        "update users set description = :d where name = :n",
        {"d": "via controlled sql", "n": "Admin"},
        instance="general",
    )
    rows = db.sql.execute(
        "select description from users where name = :n", {"n": "Admin"}, instance="general"
    )
    assert rows[0]["description"] == "via controlled sql"
