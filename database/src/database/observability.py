"""Security-relevant persistence signals (Database Principle 16): connection failure, Migration
failure, constraint violation, Transaction conflict, and protected-data access, recorded without
secret or credential values."""

from __future__ import annotations

import dataclasses
import logging

logger = logging.getLogger("database.observability")

_EVENTS: list[SignalEvent] = []


@dataclasses.dataclass(frozen=True)
class SignalEvent:
    kind: str
    detail: str


def record_event(kind: str, detail: str) -> None:
    """Record one observability signal. `detail` must never contain a secret or credential
    value (Database Principle 12 & 16) — callers pass only non-secret context."""
    event = SignalEvent(kind=kind, detail=detail)
    _EVENTS.append(event)
    logger.info("database signal: %s — %s", kind, detail)


def recorded_events() -> tuple[SignalEvent, ...]:
    """Read-only access to recorded signals (used by tests and diagnostics)."""
    return tuple(_EVENTS)


def clear_events() -> None:
    """Testing utility: reset the in-process signal log between test cases."""
    _EVENTS.clear()
