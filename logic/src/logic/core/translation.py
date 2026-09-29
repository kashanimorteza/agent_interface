"""Translation of what Database raises into Application Outcomes."""

import re
from typing import Any

from sqlalchemy import exc

from logic.core.outcome import Outcome, OutcomeKind

_UNIQUE = "23505"
_REFERENCE = "23503"
_REFUSED_STATEMENT = re.compile(
    r"syntax error|no such column|no such function|unrecognized token|incomplete input|"
    r"wrong number of bindings|missing parameter",
    re.IGNORECASE,
)


def translate(error: Exception) -> Outcome[Any] | None:
    """Turn an expected Database failure into its Application Outcome.

    Args:
        error (Exception): Failure raised by a call into Database.

    Returns:
        (Outcome | None): The matching failure Outcome, or None when the failure is not an expected one.
    """
    if isinstance(error, exc.IntegrityError):
        return _integrity(error)
    if isinstance(error, ValueError | TypeError):
        return _invalid(f"Database refused the request: {error}")
    if isinstance(error, exc.OperationalError):
        if _REFUSED_STATEMENT.search(str(error.orig)):
            return _invalid("Database refused the command as malformed")
        return _unavailable()
    if isinstance(error, exc.DataError | exc.ProgrammingError):
        return _invalid("Database refused the request as invalid")
    if isinstance(error, exc.DBAPIError | exc.TimeoutError | OSError):
        return _unavailable()
    if isinstance(
        error, exc.StatementError | exc.ArgumentError | exc.InvalidRequestError
    ):
        return _invalid("Database refused the request as invalid")
    return None


def _integrity(error: exc.IntegrityError) -> Outcome[Any]:
    state = getattr(error.orig, "sqlstate", None)
    text = str(error.orig).upper()
    if state == _UNIQUE or "UNIQUE CONSTRAINT" in text:
        return Outcome.failure(
            OutcomeKind.CONFLICT,
            "a stored record already holds one of the unique values",
        )
    if state == _REFERENCE or "FOREIGN KEY" in text:
        return Outcome.failure(
            OutcomeKind.BROKEN_REFERENCE,
            "the request refers to a record that does not exist, or the record is still referred to by another",
        )
    return _invalid("the request breaks a rule the stored data enforces")


def _invalid(reason: str) -> Outcome[Any]:
    return Outcome.failure(OutcomeKind.INVALID, reason)


def _unavailable() -> Outcome[Any]:
    return Outcome.failure(
        OutcomeKind.UNAVAILABLE, "the stored data could not be reached"
    )
