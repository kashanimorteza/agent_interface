"""After-generation preparation: the configured commands, in order, on one Instance."""

from collections.abc import Sequence

from database.core import data
from database.core._cli import run
from database.core._contracts import DatabaseInstance, LifecycleResult
from database.core._failures import DatabaseError, LifecycleFailure, sanitized
from database.core.initial_data import insert_initial_data
from database.core.tables import create_tables

_COMMANDS = {"create_tables": create_tables, "insert_initial_data": insert_initial_data}


@sanitized
def prepare(instance: DatabaseInstance | None = None) -> list[LifecycleResult]:
    """Run the configured commands in order on the configured Instance.

    A failed command stops preparation, so a later command never runs after it. The
    failure names the Instance and the command. Returns nothing when disabled.
    """
    settings = data.configuration().after_generation
    if not settings.enabled:
        return []
    member = DatabaseInstance(settings.instance)
    results: list[LifecycleResult] = []
    for name in settings.commands:
        try:
            results.append(_COMMANDS[name](member))
        except DatabaseError as error:
            message = (
                f"Preparation failed on Instance {member.value} "
                f"in {name}: {error.message}"
            )
            if settings.fail_on_error:
                raise LifecycleFailure(message) from None
            results.append(LifecycleResult(name, member, False, None, message))
            break
    return results


def main(argv: Sequence[str] | None = None) -> int:
    """Run the after-generation preparation by hand."""
    return run(
        "Prepare the default Instance as after generation.",
        lambda _: prepare(),
        argv,
        with_instance=False,
    )
