"""Security-relevant persistence signals (Database Principle 16).

Every signal is a plain, structured log record on a dedicated logger. No signal ever
carries a secret value: callers pass only non-secret identifiers (table names, field
names, Database Instance identities), never a credential value or connection secret.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("database.signals")


def _emit(signal: str, **fields: Any) -> None:
    logger.info("%s %s", signal, fields)


def connection_failure(instance: str, reason: str) -> None:
    _emit("connection_failure", instance=instance, reason=reason)


def migration_failure(reason: str) -> None:
    _emit("migration_failure", reason=reason)


def constraint_violation(model: str, constraint: str) -> None:
    _emit("constraint_violation", model=model, constraint=constraint)


def transaction_conflict(instance: str, reason: str) -> None:
    _emit("transaction_conflict", instance=instance, reason=reason)


def protected_data_access(model: str, fields: tuple[str, ...], operation: str) -> None:
    _emit("protected_data_access", model=model, fields=fields, operation=operation)


def controlled_command_executed(name: str) -> None:
    _emit("controlled_command_executed", name=name)
