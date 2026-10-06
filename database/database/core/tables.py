"""Core Tables: coordinates the CreateTables Lifecycle Command.

Tables come only from the Entities of the Model Entity Collection and the Declarations they expose.
The Target is never read, and an existing Table that differs is reported, never changed.
"""

from model.interface import entities as _entities

from database.core.data import Data
from database.core.values import DatabaseInstance, LifecycleResult

COMMAND = "create_tables"


def create_tables(data: Data, instance: DatabaseInstance | None) -> LifecycleResult:
    selected = data.instance(instance)
    member = DatabaseInstance[selected.member]
    engine = data.engine(selected)
    entity_classes = list(_entities)
    differences = engine.differences(entity_classes)
    if differences:
        detail = "; ".join(f"{name}: {', '.join(items)}" for name, items in differences.items())
        message = f"Stopped, a Table differs from its Declaration ({detail})"
        return LifecycleResult(COMMAND, member, False, None, message)
    counts = engine.create_tables(entity_classes)
    message = f"Created {counts['created']} Tables; {counts['existing']} already matched"
    return LifecycleResult(COMMAND, member, True, len(entity_classes), message)
