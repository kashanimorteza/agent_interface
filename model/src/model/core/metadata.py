"""Validation of Entity Metadata: every reference resolves and nothing is ambiguous."""

from collections.abc import Sequence

from pydantic import TypeAdapter, ValidationError

from model.core.declaration import Declaration, FieldDeclaration
from model.core.naming import entity_name, field_name
from model.core.types import python_type

SENSITIVITY_MARKERS = frozenset({"password", "sensitive"})
VALUE_GENERATIONS = frozenset({"auto_increment"})
CONSTRAINTS = frozenset({"size"})


def _duplicates(items: Sequence[object]) -> list[object]:
    return [item for index, item in enumerate(items) if item in items[:index]]


def _field_problems(owner: str, field: FieldDeclaration) -> list[str]:
    where = f"{owner}.{field.name}"
    problems: list[str] = []
    try:
        realization = python_type(field.type)
    except ValueError as error:
        return [f"{where}: {error}"]
    if field.sensitivity is not None and field.sensitivity not in SENSITIVITY_MARKERS:
        problems.append(
            f"{where}: unrecognized Sensitivity Marker {field.sensitivity!r}."
        )
    if field.value_generation is not None:
        if field.value_generation not in VALUE_GENERATIONS:
            problems.append(
                f"{where}: unrecognized Value Generation {field.value_generation!r}."
            )
        elif field.type != "integer":
            problems.append(f"{where}: auto_increment requires the integer Type.")
        if field.has_default:
            problems.append(
                f"{where}: a Field cannot have both a Default Value and Value Generation."
            )
    if not field.has_default and field.default is not None:
        problems.append(f"{where}: a default is given but has_default is false.")
    if field.has_default:
        if field.default is None:
            if not field.nullable:
                problems.append(
                    f"{where}: a non-nullable Field cannot default to null."
                )
        else:
            try:
                TypeAdapter(realization).validate_python(field.default, strict=True)
            except ValidationError:
                problems.append(
                    f"{where}: the default does not satisfy the {field.type} Type."
                )
    for name, value in field.constraints.items():
        if name not in CONSTRAINTS:
            problems.append(f"{where}: unrecognized constraint {name!r}.")
        elif (
            field.type != "string"
            or isinstance(value, bool)
            or not isinstance(value, int)
            or value < 1
        ):
            problems.append(
                f"{where}: size must be a positive integer on a string Field."
            )
    return problems


def _name_problems(declaration: Declaration) -> list[str]:
    problems: list[str] = []
    try:
        entity_name(declaration.name)
    except ValueError as error:
        problems.append(str(error))
    physical: dict[str, str] = {}
    for field in declaration.fields:
        try:
            name = field_name(field.name)
        except ValueError as error:
            problems.append(f"{declaration.name}: {error}")
            continue
        if name in physical:
            problems.append(
                f"{declaration.name}: Fields {physical[name]!r} and {field.name!r} share the physical name {name!r}."
            )
        physical[name] = field.name
    return problems


def entity_problems(declaration: Declaration) -> list[str]:
    """Return every problem found in one Entity's Declaration, each naming its item."""
    owner = declaration.name
    names = [field.name for field in declaration.fields]
    known = set(names)
    fields = {field.name: field for field in declaration.fields}
    problems = _name_problems(declaration)
    for name in _duplicates(names):
        problems.append(f"{owner}: Field {name!r} is declared more than once.")
    identity = fields.get("id")
    if identity is None:
        problems.append(f"{owner}: the mandatory Field 'id' is missing.")
    elif identity.nullable or not identity.immutable:
        problems.append(f"{owner}: 'id' must be non-nullable and immutable.")
    activity = fields.get("is_active")
    if activity is None:
        problems.append(f"{owner}: the mandatory Field 'is_active' is missing.")
    elif activity.type != "boolean" or activity.nullable or activity.immutable:
        problems.append(
            f"{owner}: 'is_active' must be a non-nullable, mutable boolean."
        )
    if declaration.primary_key != "id":
        problems.append(f"{owner}: the Primary Key must name 'id'.")
    for field in declaration.fields:
        problems.extend(_field_problems(owner, field))
    triples = [
        (relation.local_field, relation.target_entity, relation.target_field)
        for relation in declaration.relations
    ]
    for relation in declaration.relations:
        if relation.local_field not in known:
            problems.append(
                f"{owner}: Relation local Field {relation.local_field!r} does not exist."
            )
    for triple in _duplicates(triples):
        problems.append(f"{owner}: Relation {triple!r} is declared more than once.")
    for kind, groups in (
        ("Uniqueness Constraint", declaration.unique_constraints),
        ("Index", declaration.indexes),
    ):
        for group in groups:
            if not group:
                problems.append(f"{owner}: a {kind} names no Field.")
            for name in sorted(set(group) - known):
                problems.append(
                    f"{owner}: {kind} {group!r} names unknown Field {name!r}."
                )
            for name in _duplicates(group):
                problems.append(f"{owner}: {kind} {group!r} repeats Field {name!r}.")
        for group in _duplicates(groups):
            problems.append(f"{owner}: {kind} {group!r} is declared more than once.")
    return problems


def model_problems(declarations: Sequence[Declaration]) -> list[str]:
    """Return every problem found across all Entities, including unresolved Relations."""
    by_name = {declaration.name: declaration for declaration in declarations}
    problems: list[str] = []
    for name in _duplicates([declaration.name for declaration in declarations]):
        problems.append(f"Entity {name!r} is declared more than once.")
    physical: dict[str, str] = {}
    for declaration in declarations:
        problems.extend(entity_problems(declaration))
        try:
            name = entity_name(declaration.name)
        except ValueError:
            name = ""
        if name and name in physical and physical[name] != declaration.name:
            problems.append(
                f"Entities {physical[name]!r} and {declaration.name!r} share the physical name {name!r}."
            )
        if name:
            physical[name] = declaration.name
        local_fields = {field.name: field for field in declaration.fields}
        for relation in declaration.relations:
            target = by_name.get(relation.target_entity)
            where = f"{declaration.name}: Relation {relation.local_field!r}"
            if target is None:
                problems.append(
                    f"{where} targets unknown Entity {relation.target_entity!r}."
                )
                continue
            target_field = {field.name: field for field in target.fields}.get(
                relation.target_field
            )
            if target_field is None:
                problems.append(
                    f"{where} targets unknown Field {relation.target_entity}.{relation.target_field}."
                )
                continue
            local = local_fields.get(relation.local_field)
            if local is not None and local.type != target_field.type:
                problems.append(
                    f"{where} joins the {local.type} Type to {relation.target_entity}.{relation.target_field} of Type {target_field.type}."
                )
    return problems


def validate_entity(declaration: Declaration) -> None:
    """Reject one Entity's Declaration when any of its metadata is invalid."""
    problems = entity_problems(declaration)
    if problems:
        raise ValueError("Invalid Entity Metadata:\n- " + "\n- ".join(problems))


def validate_model(declarations: Sequence[Declaration]) -> None:
    """Reject the complete set of Declarations when any metadata is invalid."""
    problems = model_problems(declarations)
    if problems:
        raise ValueError("Invalid Model Metadata:\n- " + "\n- ".join(problems))
