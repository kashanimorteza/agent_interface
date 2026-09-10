"""Declaration capabilities shared by every domain Model.

Internal module: consumers read declarations through the classes exported by the
package's public interface, never by importing this module.
"""

import dataclasses
import enum
import types
import typing
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar, Final, Self

from pydantic import BaseModel, ConfigDict, Field, GetCoreSchemaHandler, GetJsonSchemaHandler, model_validator
from pydantic_core import core_schema


class _NotDeclared:
    """Marks a declaration property the Model neither states nor inherits from a default."""

    _instance: "_NotDeclared | None" = None

    def __new__(cls) -> "_NotDeclared":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "NOT_DECLARED"

    def __bool__(self) -> bool:
        return False

    def __reduce__(self) -> tuple[type, tuple[()]]:
        return (_NotDeclared, ())


NOT_DECLARED: Final = _NotDeclared()
"""The value of a declaration property that is absent: neither stated nor defaulted."""


# --------------------------------------------------------------------------- field properties


class LogicalType(enum.StrEnum):
    """Logical type of a field, independent of any storage or transport form."""

    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DECIMAL = "decimal"
    DATETIME = "datetime"


_PYTHON_TYPES: Final[Mapping[LogicalType, type]] = {
    LogicalType.INTEGER: int,
    LogicalType.STRING: str,
    LogicalType.BOOLEAN: bool,
    LogicalType.FLOAT: float,
    LogicalType.DECIMAL: Decimal,
    LogicalType.DATETIME: datetime,
}


class AtRestMode(enum.StrEnum):
    """The persistence transformation a credential field requires at rest."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class GenerationMethod(enum.StrEnum):
    """How a value the Model leaves to generation is supplied by the Component that stores it."""

    AUTO_INCREMENT = "auto_increment"
    SECURE = "secure"


class AwaitingGeneration:
    """A field value that is declared to be generated and has not been generated yet.

    It is distinct from an absent value and from an explicit null, and a field holding it
    is pending: it never counts as satisfied. Immutable and compared by its method.
    """

    # A plain class rather than a dataclass: Pydantic turns a dataclass returned by a Python-mode
    # serializer into a mapping, which would lose the marker in model_dump().
    __slots__ = ("_method",)

    def __init__(self, method: GenerationMethod) -> None:
        object.__setattr__(self, "_method", GenerationMethod(method))

    @property
    def method(self) -> GenerationMethod:
        return self._method

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("AwaitingGeneration is immutable")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AwaitingGeneration):
            return NotImplemented
        return other._method is self._method

    def __hash__(self) -> int:
        return hash((AwaitingGeneration, self._method))

    def __repr__(self) -> str:
        return f"AwaitingGeneration({self._method.value!r})"

    def __reduce__(self) -> tuple[type, tuple[GenerationMethod]]:
        return (AwaitingGeneration, (self._method,))

    @classmethod
    def __get_pydantic_core_schema__(cls, source: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        # The serialized form {"awaiting_generation": method} validates back into the marker, so a
        # pending record survives a JSON round trip; a Python dump keeps the marker itself. The
        # serializer sits on every inner schema because a union serializes through its members.
        serialization = core_schema.plain_serializer_function_ser_schema(_serialize_awaiting, info_arg=True)
        from_serialized = core_schema.no_info_after_validator_function(
            lambda data: cls(GenerationMethod(data["awaiting_generation"])),
            core_schema.typed_dict_schema(
                {
                    "awaiting_generation": core_schema.typed_dict_field(
                        core_schema.literal_schema([method.value for method in GenerationMethod])
                    )
                },
                extra_behavior="forbid",
            ),
            serialization=serialization,
        )
        return core_schema.json_or_python_schema(
            json_schema=from_serialized,
            python_schema=core_schema.union_schema(
                [core_schema.is_instance_schema(cls, serialization=serialization), from_serialized]
            ),
            serialization=serialization,
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {"awaiting_generation": {"enum": [method.value for method in GenerationMethod]}},
            "required": ["awaiting_generation"],
            "additionalProperties": False,
        }


def _serialize_awaiting(value: AwaitingGeneration, info: core_schema.SerializationInfo) -> Any:
    return {"awaiting_generation": value.method.value} if info.mode_is_json() else value


@dataclasses.dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The resolved declaration of one field of a Model.

    Every property holds the resolved value: the one the project definition states, or
    the applicable default when it states none. A property with neither is NOT_DECLARED.
    """

    name: str
    logical_type: LogicalType
    nullable: bool
    primary_key: bool | _NotDeclared = NOT_DECLARED
    auto_increment: bool | _NotDeclared = NOT_DECLARED
    unique: bool | _NotDeclared = NOT_DECLARED
    default: Any = NOT_DECLARED
    size: int | _NotDeclared = NOT_DECLARED
    credential: bool | _NotDeclared = NOT_DECLARED
    at_rest: AtRestMode | _NotDeclared = NOT_DECLARED
    generation: GenerationMethod | _NotDeclared = NOT_DECLARED
    purpose: str | _NotDeclared = NOT_DECLARED

    def describe(self) -> dict[str, Any]:
        """Return the declared properties as plain data, omitting absent ones."""
        described: dict[str, Any] = {}
        for item in dataclasses.fields(self):
            value = getattr(self, item.name)
            if value is NOT_DECLARED:
                continue
            if isinstance(value, enum.Enum):
                value = value.value
            elif isinstance(value, Decimal):
                value = str(value)
            elif isinstance(value, datetime):
                value = value.isoformat()
            described[item.name] = value
        return described


class _DeclarationCarrier:
    """Keeps a field's declaration on its Pydantic field and publishes it in JSON Schema."""

    __slots__ = ("declaration",)

    def __init__(self, declaration: FieldDeclaration) -> None:
        self.declaration = declaration

    def __call__(self, schema: dict[str, Any]) -> None:
        described = self.declaration.describe()
        described.pop("name", None)
        schema["x-declaration"] = described


def field(
    logical_type: LogicalType,
    *,
    nullable: bool,
    primary_key: bool | _NotDeclared = NOT_DECLARED,
    auto_increment: bool | _NotDeclared = NOT_DECLARED,
    unique: bool | _NotDeclared = NOT_DECLARED,
    default: Any = NOT_DECLARED,
    size: int | _NotDeclared = NOT_DECLARED,
    credential: bool | _NotDeclared = NOT_DECLARED,
    at_rest: AtRestMode | _NotDeclared = NOT_DECLARED,
    generation: GenerationMethod | _NotDeclared = NOT_DECLARED,
    purpose: str | _NotDeclared = NOT_DECLARED,
) -> Any:
    """Declare one Model field with its resolved properties."""
    if at_rest is not NOT_DECLARED and credential is not True:
        raise TypeError("an at-rest mode is declared only for a credential field")
    if auto_increment is True:
        if generation not in (NOT_DECLARED, GenerationMethod.AUTO_INCREMENT):
            raise TypeError("an auto-increment field is generated by auto increment")
        generation = GenerationMethod.AUTO_INCREMENT
    declaration = FieldDeclaration(
        name="",
        logical_type=LogicalType(logical_type),
        nullable=nullable,
        primary_key=primary_key,
        auto_increment=auto_increment,
        unique=unique,
        default=default,
        size=size,
        credential=credential,
        at_rest=AtRestMode(at_rest) if at_rest is not NOT_DECLARED else NOT_DECLARED,
        generation=GenerationMethod(generation) if generation is not NOT_DECLARED else NOT_DECLARED,
        purpose=purpose,
    )
    options: dict[str, Any] = {"json_schema_extra": _DeclarationCarrier(declaration)}
    if purpose is not NOT_DECLARED:
        options["description"] = purpose
    if size is not NOT_DECLARED:
        options["max_length"] = size
    if credential is True:
        options["repr"] = False
    if default is not NOT_DECLARED:
        options["default"] = default
    elif declaration.generation is GenerationMethod.AUTO_INCREMENT:
        options["default"] = AwaitingGeneration(GenerationMethod.AUTO_INCREMENT)
    elif nullable:
        # Omission is accepted for a nullable field without a declared default; whether the
        # value was supplied at all stays visible through model_fields_set.
        options["default"] = None
    return Field(**options)


# --------------------------------------------------------------------------- relationships


class RelationshipKind(enum.StrEnum):
    """Whether the declaring Model belongs to the related Model or only uses it."""

    BELONGS_TO = "belongs_to"
    USES = "uses"


class Cardinality(enum.StrEnum):
    """How many records on each side a relationship connects, read from the declaring Model."""

    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"


class Participation(enum.StrEnum):
    """Whether every record on one side must take part in the relationship."""

    REQUIRED = "required"
    OPTIONAL = "optional"


@dataclasses.dataclass(frozen=True, slots=True)
class Relationship:
    """One declared connection from the declaring Model to a related Model."""

    role: str
    """The role the related Model plays for the declaring Model."""
    target: type["DomainModel"]
    field: str
    """The logical field of the declaring Model that carries the connection."""
    kind: RelationshipKind
    cardinality: Cardinality
    source_participation: Participation
    """Whether every record of the declaring Model must be connected."""
    target_participation: Participation
    """Whether every record of the related Model must be connected."""
    inverse_role: str | _NotDeclared = NOT_DECLARED
    """The role the declaring Model plays for the related Model, when the definition names one."""
    statement: str | _NotDeclared = NOT_DECLARED
    """The relationship as the project definition states it."""


# --------------------------------------------------------------------------- rules


class RuleKind(enum.StrEnum):
    """The form of a declared rule."""

    UNIQUE_TOGETHER = "unique_together"
    GENERAL = "general"


class RuleRequirement(enum.StrEnum):
    """What evaluating a rule needs beyond one Model's own data."""

    STORED_STATE = "stored_state"
    APPLICATION_CONTEXT = "application_context"


@dataclasses.dataclass(frozen=True, slots=True)
class RuleDeclaration:
    """A rule the Model declares but its own validation does not evaluate."""

    name: str
    kind: RuleKind
    fields: tuple[str, ...]
    requires: RuleRequirement
    statement: str
    """The rule as the project definition states it."""


def unique_together(*fields: str, statement: str) -> RuleDeclaration:
    """Declare that a combination of fields must be unique across records."""
    return RuleDeclaration(
        name="unique_" + "_".join(fields),
        kind=RuleKind.UNIQUE_TOGETHER,
        fields=tuple(fields),
        requires=RuleRequirement.STORED_STATE,
        statement=statement,
    )


def rule(name: str, fields: tuple[str, ...], requires: RuleRequirement, *, statement: str) -> RuleDeclaration:
    """Declare any other rule that needs stored state or application context to evaluate."""
    return RuleDeclaration(
        name=name,
        kind=RuleKind.GENERAL,
        fields=tuple(fields),
        requires=RuleRequirement(requires),
        statement=statement,
    )


# --------------------------------------------------------------------------- Model base


@dataclasses.dataclass(frozen=True, slots=True)
class _ResolvedDeclarations:
    fields: Mapping[str, FieldDeclaration]
    relationships: tuple[Relationship, ...]
    rules: tuple[RuleDeclaration, ...]


_DECLARATIONS: dict[type, _ResolvedDeclarations] = {}


def _union_members(annotation: Any) -> set[Any]:
    if isinstance(annotation, types.UnionType) or typing.get_origin(annotation) is typing.Union:
        return set(typing.get_args(annotation))
    return {annotation}


def _resolve_fields(model: type["DomainModel"]) -> Mapping[str, FieldDeclaration]:
    declarations: dict[str, FieldDeclaration] = {}
    for name, info in model.model_fields.items():
        carrier = info.json_schema_extra
        if not isinstance(carrier, _DeclarationCarrier):
            raise TypeError(f"{model.__name__}.{name} has no field declaration")
        declaration = dataclasses.replace(carrier.declaration, name=name)
        expected = {_PYTHON_TYPES[declaration.logical_type]}
        if declaration.nullable:
            expected.add(types.NoneType)
        if declaration.generation is not NOT_DECLARED:
            expected.add(AwaitingGeneration)
        actual = _union_members(info.annotation)
        if actual != expected:
            raise TypeError(
                f"{model.__name__}.{name} is annotated {info.annotation!r}, which contradicts its declared "
                f"{declaration.logical_type.value} type, nullable={declaration.nullable}, "
                f"generation={declaration.generation!r}"
            )
        if declaration.default is not NOT_DECLARED:
            if info.is_required() or info.default != declaration.default:
                raise TypeError(f"{model.__name__}.{name} does not apply its declared default")
        elif declaration.generation is GenerationMethod.AUTO_INCREMENT:
            if info.is_required() or info.default != AwaitingGeneration(GenerationMethod.AUTO_INCREMENT):
                raise TypeError(f"{model.__name__}.{name} must await its auto-increment value when omitted")
        elif declaration.nullable:
            if info.is_required() or info.default is not None:
                raise TypeError(f"{model.__name__}.{name} must accept omission as a nullable field")
        elif not info.is_required():
            raise TypeError(f"{model.__name__}.{name} supplies a default it does not declare")
        declarations[name] = declaration
    return types.MappingProxyType(declarations)


def _resolve_relationships(model: type["DomainModel"], fields: Mapping[str, FieldDeclaration]) -> tuple[Relationship, ...]:
    relationships = tuple(model.declared_relationships)
    roles: set[str] = set()
    for relationship in relationships:
        where = f"{model.__name__} relationship {relationship.role!r}"
        if not isinstance(relationship, Relationship):
            raise TypeError(f"{model.__name__} declares a relationship that is not a Relationship")
        if not (isinstance(relationship.target, type) and issubclass(relationship.target, DomainModel)):
            raise TypeError(f"{where} does not relate to a domain Model")
        if relationship.role in roles:
            raise TypeError(f"{where} repeats a role")
        roles.add(relationship.role)
        carrier = fields.get(relationship.field)
        if carrier is None:
            raise TypeError(f"{where} is carried by {relationship.field!r}, which is not a field")
        if carrier.logical_type is not LogicalType.INTEGER:
            raise TypeError(f"{where} is carried by a field that cannot hold an identifier")
        expected = Participation.OPTIONAL if carrier.nullable else Participation.REQUIRED
        if relationship.source_participation is not expected:
            raise TypeError(f"{where} states participation that contradicts the nullability of its field")
    return relationships


def _resolve_rules(model: type["DomainModel"], fields: Mapping[str, FieldDeclaration]) -> tuple[RuleDeclaration, ...]:
    rules = tuple(model.declared_rules)
    names: set[str] = set()
    for declared in rules:
        if not isinstance(declared, RuleDeclaration):
            raise TypeError(f"{model.__name__} declares a rule that is not a RuleDeclaration")
        if declared.name in names:
            raise TypeError(f"{model.__name__} repeats rule {declared.name!r}")
        names.add(declared.name)
        missing = [name for name in declared.fields if name not in fields]
        if missing or not declared.fields:
            raise TypeError(f"{model.__name__} rule {declared.name!r} names fields it does not have: {missing}")
    return rules


class DomainModel(BaseModel):
    """Base of every domain Model: validates its own data and publishes its declarations."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True, validate_default=True)

    logical_name: ClassVar[str]
    """The Model's logical identity as the project definition names it."""
    declared_relationships: ClassVar[tuple[Relationship, ...]] = ()
    declared_rules: ClassVar[tuple[RuleDeclaration, ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        logical_name = getattr(cls, "logical_name", None)
        if not isinstance(logical_name, str) or not logical_name:
            raise TypeError(f"{cls.__name__} must state its logical_name")
        fields = _resolve_fields(cls)
        _DECLARATIONS[cls] = _ResolvedDeclarations(
            fields=fields,
            relationships=_resolve_relationships(cls, fields),
            rules=_resolve_rules(cls, fields),
        )

    @classmethod
    def field_declarations(cls) -> Mapping[str, FieldDeclaration]:
        """Return every field's resolved declaration, keyed by field name in declared order."""
        return _DECLARATIONS[cls].fields

    @classmethod
    def credential_fields(cls) -> Mapping[str, FieldDeclaration]:
        """Return the declarations of the fields that are credentials, in declared order."""
        return types.MappingProxyType(
            {name: declaration for name, declaration in cls.field_declarations().items() if declaration.credential is True}
        )

    @classmethod
    def relationship_declarations(cls) -> tuple[Relationship, ...]:
        """Return every declared relationship of the Model, in declared order."""
        return _DECLARATIONS[cls].relationships

    @classmethod
    def relationship_for(cls, field_name: str) -> Relationship | None:
        """Return the relationship carried by a field, or None when the field carries none."""
        return next((item for item in cls.relationship_declarations() if item.field == field_name), None)

    @classmethod
    def rule_declarations(cls) -> tuple[RuleDeclaration, ...]:
        """Return the rules the Model declares that its own validation does not evaluate."""
        return _DECLARATIONS[cls].rules

    def pending_fields(self) -> frozenset[str]:
        """Return the fields whose values await declared generation."""
        return frozenset(name for name in type(self).model_fields if isinstance(getattr(self, name), AwaitingGeneration))

    def is_complete(self) -> bool:
        """Return whether no field of this record still awaits generation."""
        return not self.pending_fields()

    @model_validator(mode="after")
    def check_awaiting_generation(self) -> Self:
        declarations = type(self).field_declarations()
        for name, declaration in declarations.items():
            value = getattr(self, name)
            if isinstance(value, AwaitingGeneration) and value.method is not declaration.generation:
                raise ValueError(f"{name} does not declare generation by {value.method.value}")
        return self
