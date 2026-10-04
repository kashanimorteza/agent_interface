"""Core Tables: coordinates the CreateTables Lifecycle Command."""

from enum import Enum

from database.core import data


def create_tables(instance: Enum | None = None) -> data.LifecycleResult:
    """Create every Table of the Model Entity Collection on the selected Instance."""
    spec = data.resolve_instance(instance)
    unit, handle = data.connection_for(spec)
    try:
        processed, created = unit.create_tables(handle, data.entity_collection)
    except data.ExecutionError:
        if getattr(unit, "ATOMIC_STRUCTURE_CHANGES", False):
            raise
        raise data.LifecycleError(
            f"Table creation ended in an incomplete state on Instance '{spec.key}'."
        ) from None
    return data.LifecycleResult(
        "create_tables",
        data.instance_member(spec),
        True,
        processed,
        f"{created} of {processed} Tables created.",
    )
