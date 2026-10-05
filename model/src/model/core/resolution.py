from collections.abc import Sequence

from model.core.columns import physical_name
from model.core.declaration import Declaration


def verify_relations(declarations: Sequence[Declaration]) -> None:
    by_name = {declaration.name: declaration for declaration in declarations}
    if len(by_name) != len(declarations):
        raise ValueError("Entity names must be unique across the Model.")
    physical: dict[str, str] = {}
    for declaration in declarations:
        name = physical_name(declaration.name)
        if name in physical:
            raise ValueError(
                f"Entities '{physical[name]}' and '{declaration.name}' share the physical name '{name}'."
            )
        physical[name] = declaration.name
    for declaration in declarations:
        local_fields = {field.name: field for field in declaration.fields}
        for relation in declaration.relations:
            target = by_name.get(relation.target_entity)
            if target is None:
                raise ValueError(
                    f"Entity '{declaration.name}': Relation on '{relation.local_field}' names unknown Entity '{relation.target_entity}'."
                )
            target_field = next(
                (
                    field
                    for field in target.fields
                    if field.name == relation.target_field
                ),
                None,
            )
            if target_field is None:
                raise ValueError(
                    f"Entity '{declaration.name}': Relation on '{relation.local_field}' names unknown Field '{relation.target_entity}.{relation.target_field}'."
                )
            if local_fields[relation.local_field].type is not target_field.type:
                raise ValueError(
                    f"Entity '{declaration.name}': Relation on '{relation.local_field}' has a Type incompatible with '{relation.target_entity}.{relation.target_field}'."
                )
