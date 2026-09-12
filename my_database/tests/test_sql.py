"""The controlled SQL execution route."""

import my_model
import pytest

import my_database


def test_parameterized_select_returns_protected_results() -> None:
    created = my_database.add(
        my_model.User(id=0, name="Admin", username="admin", password="x", api_key="y")
    )
    rows = my_database.execute_controlled_sql(
        "SELECT id, name, password FROM users WHERE id = :id", {"id": created.id}, table="users"
    )
    assert rows == [{"id": created.id, "name": "Admin", "password": "<redacted>"}]


def test_structural_change_is_rejected_before_execution() -> None:
    with pytest.raises(my_database.errors.ControlledSQLRejectedError):
        my_database.execute_controlled_sql(
            "ALTER TABLE users ADD COLUMN hacked TEXT", {}, table="users"
        )
    # Prove it never executed: the table still lacks the column.
    rows = my_database.execute_controlled_sql("SELECT id FROM users", {}, table="users")
    assert rows == []


def test_unknown_table_is_rejected() -> None:
    with pytest.raises(my_database.errors.ControlledSQLRejectedError):
        my_database.execute_controlled_sql("SELECT * FROM sqlite_master", {}, table="sqlite_master")


def test_parameterized_insert_through_controlled_sql_and_transaction_participation() -> None:
    with my_database.transaction() as session:
        my_database.execute_controlled_sql(
            "INSERT INTO trading_platforms (name, code, status, description) "
            "VALUES (:name, :code, 1, NULL)",
            {"name": "Binance", "code": "binance"},
            table="trading_platforms",
            session=session,
        )
    platforms = my_database.list_records(my_model.TradingPlatform)
    assert [p.code for p in platforms] == ["binance"]
