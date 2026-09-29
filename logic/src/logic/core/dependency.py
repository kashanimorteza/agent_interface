"""Bounded use of a dependency: every call waits at most a finite time."""

from collections.abc import Callable
from threading import Thread
from typing import Any

from logic.core.configuration import Configuration
from logic.core.outcome import Outcome, OutcomeKind
from logic.core.translation import translate


class Dependency:
    """Run calls into a dependency and answer each with an Outcome."""

    def __init__(self, configuration: Configuration) -> None:
        """Take the finite bounds from the configuration.

        Args:
            configuration (Configuration): Validated runtime configuration.
        """
        self._timeout = configuration.dependency_timeout_seconds
        self._retries = configuration.dependency_retries

    def call[T](
        self, action: Callable[[], T], *, repeatable: bool = False
    ) -> Outcome[T]:
        """Run a call, waiting at most the configured time for each attempt.

        Args:
            action (Callable): Call into the dependency.
            repeatable (bool): Whether repeating the call is safe or idempotent; only then is an unavailable dependency retried, at most the configured number of times.

        Returns:
            (Outcome): A success holding the answer, or the failure Outcome an expected failure translates to.
        """
        outcome = self._attempt(action)
        for _ in range(self._retries if repeatable else 0):
            if outcome.kind is not OutcomeKind.UNAVAILABLE:
                break
            outcome = self._attempt(action)
        return outcome

    def _attempt(self, action: Callable[[], Any]) -> Outcome[Any]:
        answer: list[tuple[bool, Any]] = []

        def run() -> None:
            try:
                answer.append((True, action()))
            except Exception as error:
                answer.append((False, error))

        worker = Thread(target=run, daemon=True)
        worker.start()
        worker.join(self._timeout)
        if not answer:
            return Outcome.failure(
                OutcomeKind.UNAVAILABLE,
                f"the stored data did not answer within {self._timeout:g} seconds",
            )
        succeeded, payload = answer[0]
        if succeeded:
            return Outcome.success(payload)
        outcome = translate(payload)
        if outcome is None:
            raise payload
        return outcome
