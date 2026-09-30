"""Shared manual entry point behaviour: parse an optional Instance, run, report."""

import argparse
import sys
from collections.abc import Callable, Sequence

from database.core._contracts import DatabaseInstance, LifecycleResult
from database.core._failures import DatabaseError


def run(
    description: str,
    command: Callable[
        [DatabaseInstance | None], list[LifecycleResult] | LifecycleResult
    ],
    argv: Sequence[str] | None = None,
    *,
    with_instance: bool = True,
) -> int:
    """Invoke a public command by hand and report its result; non-zero means failure."""
    parser = argparse.ArgumentParser(description=description)
    if with_instance:
        parser.add_argument(
            "--instance",
            choices=[member.value for member in DatabaseInstance],
            help="Instance to use; defaults to the configured default Instance.",
        )
    arguments = parser.parse_args(argv)
    selected = (
        DatabaseInstance(arguments.instance)
        if with_instance and arguments.instance
        else None
    )
    try:
        outcome = command(selected)
    except DatabaseError as error:
        print(f"{error.meaning}: {error.message}", file=sys.stderr)
        return 1
    for result in outcome if isinstance(outcome, list) else [outcome]:
        state = "ok" if result.success else "failed"
        print(
            f"{result.command} on {result.instance.value}: {state} - {result.message}"
        )
    return 0
