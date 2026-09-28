"""Rules that Data applies to a request, driven by the Entity's Model Declaration, before an Engine stores it."""

from typing import Any
from uuid import uuid4

from model.declaration import Generation


def new_record(entity: Any) -> Any:
    """Return a new Entity instance ready to store.

    Value Generation is applied first, then Default Values for omitted Fields, then the required and
    nullability Rules are enforced.

    Args:
        entity (Any): Entity instance supplied for a new record.

    Returns:
        (Any): A new Entity instance of the same class; the supplied instance is left unchanged.
    """
    entity_class = type(entity)
    declaration = entity_class.declaration
    values: dict[str, Any] = {}
    for field in declaration.fields:
        if field.generation is Generation.AUTO_INCREMENT:
            continue
        if field.generation is Generation.GENERATED_IDENTIFIER:
            values[field.name] = str(uuid4())
            continue
        omitted = field.name not in entity.model_fields_set
        value = (
            field.default
            if omitted and field.has_default
            else getattr(entity, field.name, None)
        )
        if value is None and not field.nullable:
            raise ValueError(
                f"{declaration.entity}.{field.name} is required and cannot be null"
            )
        values[field.name] = value
    return entity_class(**values)


def update_values(entity: Any) -> tuple[Any, dict[str, Any]]:
    """Return the record to update and the values to change.

    Only Fields supplied on the instance change. The `id` locates the record and is never changed, and a
    Field the Declaration marks immutable is never changed.

    Args:
        entity (Any): Entity instance holding the `id` and the changed values.

    Returns:
        (Any): The `id` of the record to update.
        (dict[str, Any]): Field name to new value, for the supplied mutable Fields.
    """
    declaration = type(entity).declaration
    record_id = getattr(entity, declaration.primary_key, None)
    if record_id is None:
        raise ValueError(
            f"Update needs the '{declaration.primary_key}' of the record to change"
        )
    mutable = {
        f.name
        for f in declaration.fields
        if f.name != declaration.primary_key and not f.immutable
    }
    return record_id, {
        name: getattr(entity, name) for name in entity.model_fields_set & mutable
    }
