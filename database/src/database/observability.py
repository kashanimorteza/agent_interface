"""Security-relevant persistence observability signals.

Every signal reports the event and enough context to act on it, but never a
secret value, credential representation, or full error message that could
carry one (SQLAlchemy/DBAPI error messages can echo bound values).
"""

from __future__ import annotations

import logging

logger = logging.getLogger("database")


def record_connection_failure(instance_key: str, error: BaseException) -> None:
    logger.error(
        "database.connection_failure",
        extra={"instance": instance_key, "error_type": type(error).__name__},
    )


def record_migration_failure(revision: str, error: BaseException) -> None:
    logger.error(
        "database.migration_failure",
        extra={"revision": revision, "error_type": type(error).__name__},
    )


def record_constraint_violation(table: str, error: BaseException) -> None:
    logger.warning(
        "database.constraint_violation",
        extra={"table": table, "error_type": type(error).__name__},
    )


def record_transaction_conflict(instance_key: str, error: BaseException) -> None:
    logger.warning(
        "database.transaction_conflict",
        extra={"instance": instance_key, "error_type": type(error).__name__},
    )


def record_protected_data_access(table: str, field: str) -> None:
    logger.info(
        "database.protected_data_access",
        extra={"table": table, "field": field},
    )


def record_controlled_command(name: str, table: str) -> None:
    logger.info(
        "database.controlled_command",
        extra={"command": name, "table": table},
    )
