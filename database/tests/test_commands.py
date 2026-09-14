"""Tests for the capability-restricted controlled command route (task P2-G9-T3)."""

from __future__ import annotations

import model
import pytest

from database.commands import reject_attempt
from database.exceptions import ControlledCommandRejected


def test_parameterized_command_executes_and_is_separately_observable(
    db, caplog: pytest.LogCaptureFixture
) -> None:
    user = db.create(model.User(name="Ada", username="ada", password="pw", api_key="key"))
    caplog.clear()
    caplog.set_level("INFO", logger="database.signals")
    result = db.execute_command("deactivate_user_instances", user_id=user.id)
    assert result is not None
    assert any("controlled_command_executed" in record.message for record in caplog.records)


def test_unknown_command_name_rejected(db) -> None:
    with pytest.raises(ControlledCommandRejected):
        db.execute_command("drop_all_tables")


def test_unexpected_parameter_rejected(db) -> None:
    with pytest.raises(ControlledCommandRejected):
        db.execute_command("count_positions_by_execution", user_id=1, evil_param="x")


@pytest.mark.parametrize(
    "sql",
    [
        "DROP TABLE users",
        "ALTER TABLE users ADD COLUMN hacked TEXT",
        "GRANT ALL PRIVILEGES ON users TO public",
        "PRAGMA writable_schema=1",
    ],
)
def test_structural_privilege_and_admin_statements_are_never_registered_or_reachable(
    sql: str,
) -> None:
    with pytest.raises(ControlledCommandRejected):
        reject_attempt(sql)


def test_migration_operation_is_never_reachable_through_the_command_route(db) -> None:
    with pytest.raises(ControlledCommandRejected):
        db.execute_command("upgrade_to_head")
