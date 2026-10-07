from database.core import initial_data, tables
from database.core.configuration import member_name, resolve_instance
from database.core.data import resolve
from database.core.errors import DatabaseError, LifecycleError
from database.core.values import DatabaseInstance, SetupResult


def _member(selection: DatabaseInstance | None) -> DatabaseInstance:
    return DatabaseInstance[member_name(resolve_instance(selection).key)]


def create_tables(selection: DatabaseInstance | None) -> SetupResult:
    """Create the Tables of the Model Entities on the selected Instance."""
    unit, connection = resolve(selection)
    created = tables.create_tables(unit, connection)
    total = len(tables.entity_collection())
    return SetupResult(
        command="create_tables",
        instance=_member(selection),
        success=True,
        affected=total,
        message=f"Created {created} Tables; {total - created} already matched their Entities.",
    )


def insert_initial_data(selection: DatabaseInstance | None) -> SetupResult:
    """Insert the configured Initial Data on the selected Instance."""
    unit, connection = resolve(selection)
    inserted, processed = initial_data.insert_initial_data(unit, connection)
    return SetupResult(
        command="insert_initial_data",
        instance=_member(selection),
        success=True,
        affected=processed,
        message=f"Inserted {inserted} records; {processed - inserted} were already present.",
    )


def prepare(selection: DatabaseInstance | None) -> SetupResult:
    """Create the Tables and then insert the Initial Data; stop if creating the Tables fails."""
    created = create_tables(selection)
    try:
        inserted = insert_initial_data(selection)
    except DatabaseError as error:
        raise LifecycleError(
            f"Preparation is incomplete: the Tables exist but the Initial Data was not inserted. "
            f"{error}"
        ) from None
    assert created.affected is not None and inserted.affected is not None
    return SetupResult(
        command="prepare",
        instance=created.instance,
        success=True,
        affected=created.affected + inserted.affected,
        message=f"{created.message} {inserted.message}",
    )
