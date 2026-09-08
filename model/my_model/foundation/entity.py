"""Turning a declaration into an entity that validates its own data.

An entity is declared as a set of partially stated fields together with its
relationships, its rules and the records it must start with. The declaration is
completed from the applicable defaults and becomes the entity: a type that
accepts valid domain values, refuses what it can tell is wrong from its own
values alone, and carries the rest of its declaration for the layers that
enforce or store it.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Any, ClassVar, Iterable, Mapping, Optional, Self, Union

from pydantic import BaseModel, ConfigDict, StringConstraints, create_model, model_validator

from .credentials import CredentialStorage
from .field_spec import FieldSpec, FieldType
from .generation import awaits_generation
from .initial_records import InitialRecord
from .relationships import Relationship
from .resolution import complete_fields
from .rules import DomainRule, RuleScope
from .unset import UNSET, is_stated

_PYTHON_TYPES: dict[str, type] = {
    FieldType.INTEGER: int,
    FieldType.STRING: str,
    FieldType.BOOLEAN: bool,
    FieldType.DECIMAL: Decimal,
    FieldType.FLOAT: float,
    FieldType.DATETIME: datetime,
}


class PartialView(BaseModel):
    """A view in which a field left out stays distinct from one set to nothing."""

    model_config = ConfigDict(extra="forbid")

    def stated_fields(self) -> dict[str, Any]:
        """Only the fields this view was actually given."""

        return {name: value for name, value in self.__dict__.items() if is_stated(value)}

    def states(self, field_name: str) -> bool:
        """Whether this view was given ``field_name`` at all."""

        return is_stated(self.__dict__.get(field_name, UNSET))


class Entity(BaseModel):
    """The behaviour every declared entity shares."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    entity_name: ClassVar[str] = ""
    entity_purpose: ClassVar[str] = ""
    entity_fields: ClassVar[dict[str, FieldSpec]] = {}
    relationships: ClassVar[tuple[Relationship, ...]] = ()
    rules: ClassVar[tuple[DomainRule, ...]] = ()
    initial_records: ClassVar[tuple[InitialRecord, ...]] = ()
    Partial: ClassVar[type[PartialView]]

    @model_validator(mode="after")
    def _apply_own_data_rules(self) -> Self:
        for rule in type(self).rules:
            if not rule.is_enforceable_here():
                continue
            complaint = rule.check(self)
            if complaint:
                raise ValueError(f"{rule.statement}: {complaint}")
        return self

    # <!-------------------------------------------- declaration -->

    @classmethod
    def credential_fields(cls) -> dict[str, CredentialStorage | None]:
        """The fields declared as credentials, with the treatment each requires."""

        return {
            name: spec.storage_treatment()
            for name, spec in cls.entity_fields.items()
            if spec.is_credential()
        }

    @classmethod
    def rules_for(cls, scope: RuleScope) -> tuple[DomainRule, ...]:
        """The declared rules whose enforcement needs ``scope``."""

        return tuple(rule for rule in cls.rules if rule.scope is scope)

    @classmethod
    def relationship_fields(cls) -> dict[str, Relationship]:
        """The local fields that carry a connection, keyed by field name."""

        return {r.field: r for r in cls.relationships if r.field}

    @classmethod
    def assigned_by_storage(cls, field_name: str) -> bool:
        """Whether a value for this field is produced by the layer that stores it."""

        spec = cls.entity_fields[field_name]
        return bool(is_stated(spec.auto_increment) and spec.auto_increment)

    # <!-------------------------------------------- records -->

    @classmethod
    def validate_record(cls, values: Mapping[str, Any]) -> None:
        """Check a declared record without demanding values that do not exist yet.

        A value the project requires to be generated counts as present without
        being invented, and a value the storing layer assigns need not appear.
        """

        unknown = set(values) - set(cls.entity_fields)
        if unknown:
            raise ValueError(f"{cls.entity_name}: unknown field(s) {sorted(unknown)}")

        pending = {name for name, value in values.items() if awaits_generation(value)}
        cls.Partial.model_validate({k: v for k, v in values.items() if k not in pending})

        missing = [
            name
            for name, spec in cls.entity_fields.items()
            if spec.is_required_in_state()
            and name not in values
            and not is_stated(spec.default)
            and not cls.assigned_by_storage(name)
        ]
        if missing:
            raise ValueError(f"{cls.entity_name}: record is missing {missing}")

    @classmethod
    def declared_records(cls) -> tuple[InitialRecord, ...]:
        """The records this entity must contain when the project begins."""

        return cls.initial_records


def _annotation(spec: FieldSpec) -> Any:
    base: Any = _PYTHON_TYPES[spec.type]
    if base is str and is_stated(spec.size):
        base = Annotated[str, StringConstraints(max_length=int(spec.size))]
    if is_stated(spec.nullable) and spec.nullable:
        return Optional[base]
    return base


def _default(spec: FieldSpec, assigned_by_storage: bool) -> Any:
    if is_stated(spec.default):
        return spec.default
    if assigned_by_storage or (is_stated(spec.nullable) and spec.nullable):
        return None
    return ...


def define_entity(
    *,
    name: str,
    purpose: str,
    fields: Mapping[str, FieldSpec],
    relationships: Iterable[Relationship] = (),
    rules: Iterable[DomainRule] = (),
    initial_records: Iterable[InitialRecord] = (),
) -> type[Entity]:
    """Build an entity from a declaration whose fields may be partially stated."""

    resolved = complete_fields(dict(fields))
    for field_name, spec in resolved.items():
        if not is_stated(spec.type):
            raise ValueError(f"{name}.{field_name}: no logical type is stated or defaulted")
        if spec.type not in _PYTHON_TYPES:
            raise ValueError(f"{name}.{field_name}: unknown logical type {spec.type!r}")
        if spec.is_credential() and spec.storage_treatment() is None:
            raise ValueError(
                f"{name}.{field_name}: a credential must state how it is held at rest"
            )

    definitions: dict[str, Any] = {}
    partial_definitions: dict[str, Any] = {}
    for field_name, spec in resolved.items():
        annotation = _annotation(spec)
        from_storage = bool(is_stated(spec.auto_increment) and spec.auto_increment)
        definitions[field_name] = (
            Union[annotation, None] if from_storage else annotation,
            _default(spec, from_storage),
        )
        partial_definitions[field_name] = (annotation, UNSET)

    partial = create_model(f"{name}Partial", __base__=PartialView, **partial_definitions)
    entity = create_model(name, __base__=Entity, **definitions)

    entity.entity_name = name
    entity.entity_purpose = purpose
    entity.entity_fields = resolved
    entity.relationships = tuple(relationships)
    entity.rules = tuple(rules)
    entity.initial_records = tuple(initial_records)
    entity.Partial = partial
    entity.__doc__ = purpose

    for record in entity.initial_records:
        entity.validate_record(record.values)

    return entity
