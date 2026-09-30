"""CreateTables: create or safely align every table the public Declarations require."""

from collections.abc import Sequence

from database.core import data
from database.core._cli import run
from database.core._contracts import DatabaseInstance, LifecycleResult
from database.core._failures import sanitized


@sanitized
def create_tables(instance: DatabaseInstance | None = None) -> LifecycleResult:
    """Create or align all structure on the selected Instance; safe to repeat."""
    key = data.select_instance(instance)
    aligned = data.engine_for(key).create_tables()
    return LifecycleResult(
        "create_tables",
        DatabaseInstance(key),
        True,
        aligned,
        f"{aligned} tables are aligned.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Manual entry point: invokes the public command and adds no logic of its own."""

    def command(instance: DatabaseInstance | None) -> LifecycleResult:
        from database.interface import Database

        return Database.create_tables(instance)

    return run("Create or align every Database table.", command, argv)
