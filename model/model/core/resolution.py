"""Private Entity Metadata resolution across the whole Entity set."""

from collections.abc import Iterable

from model.core.declaration import Declaration


def resolve_relations(declarations: Iterable[Declaration]) -> None:
    """Verify that every Relation names an existing Entity and Field of one Type."""
    by_name: dict[str, Declaration] = {}
    for declaration in declarations:
        if declaration.name in by_name:
            raise ValueError(f"Entity {declaration.name!r} is declared more than once")
        by_name[declaration.name] = declaration
    for declaration in by_name.values():
        local_fields = {declared.name: declared for declared in declaration.fields}
        for relation in declaration.relations:
            label = f"Entity {declaration.name!r} Relation {relation.local_field!r}"
            target = by_name.get(relation.target_entity)
            if target is None:
                raise ValueError(
                    f"{label}: target Entity {relation.target_entity!r} does not exist"
                )
            target_fields = {declared.name: declared for declared in target.fields}
            target_field = target_fields.get(relation.target_field)
            path = f"{relation.target_entity}.{relation.target_field}"
            if target_field is None:
                raise ValueError(f"{label}: target Field {path} does not exist")
            if local_fields[relation.local_field].type != target_field.type:
                raise ValueError(f"{label}: Type differs from {path}")
