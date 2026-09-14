"""The capability-restricted controlled command route.

Every command is a fixed, pre-registered, parameterized statement. A caller selects a
command by its allow-listed name and supplies only its declared parameters; there is no
path from caller input to arbitrary SQL, so a structural change, privilege change,
connection-administration action, or Migration operation can never be requested through
this route because none is ever registered.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import text

from . import observability
from .exceptions import ControlledCommandRejected
from .transaction import Transaction

_FORBIDDEN_KEYWORDS = (
    "drop",
    "alter",
    "create table",
    "grant",
    "revoke",
    "attach",
    "detach",
    "pragma",
)


def _reject_forbidden_keywords(sql: str) -> None:
    lowered = sql.lower()
    for keyword in _FORBIDDEN_KEYWORDS:
        if keyword in lowered:
            raise ControlledCommandRejected(
                f"Controlled command definitions may never contain {keyword!r}"
            )


class _Command:
    def __init__(self, name: str, sql: str, allowed_params: frozenset[str]) -> None:
        _reject_forbidden_keywords(sql)
        self.name = name
        self.statement = text(sql)
        self.allowed_params = allowed_params

    def run(self, txn: Transaction, **params: Any) -> Any:
        unexpected = set(params) - self.allowed_params
        if unexpected:
            raise ControlledCommandRejected(f"Unexpected parameters: {sorted(unexpected)}")
        result = txn.session.execute(self.statement, params)
        observability.controlled_command_executed(self.name)
        return result


_COMMANDS: dict[str, _Command] = {
    "count_positions_by_execution": _Command(
        "count_positions_by_execution",
        "SELECT is_executed, COUNT(*) AS total FROM positions "
        "WHERE user_id = :user_id GROUP BY is_executed",
        frozenset({"user_id"}),
    ),
    "deactivate_user_instances": _Command(
        "deactivate_user_instances",
        "UPDATE instances SET is_active = 0 WHERE user_id = :user_id",
        frozenset({"user_id"}),
    ),
}


def execute_command(txn: Transaction, name: str, **params: Any) -> Any:
    """Execute one allow-listed, parameterized controlled command within a Transaction."""
    try:
        command = _COMMANDS[name]
    except KeyError:
        raise ControlledCommandRejected(f"Unknown controlled command: {name!r}") from None
    return command.run(txn, **params)


def reject_attempt(sql: str, **params: Any) -> None:
    """Simulate submitting an arbitrary statement to the route: always rejected.

    The controlled command route accepts no free-form SQL from a caller; this helper
    exists only so tests can demonstrate that no path to an unregistered statement exists.
    """
    raise ControlledCommandRejected(
        "The controlled command route accepts only pre-registered command names, never SQL text"
    )
