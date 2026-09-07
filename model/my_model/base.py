"""Declaration support shared by every Model in the package.

A Model is declared as a class whose fields carry their *logical* properties
(type, identity, uniqueness, optionality, default behaviour, credential
nature, permitted generation, and meaning). Relationships, domain rules, and
initial data are declared on the class as logical declarations; the Component
responsible for each resolves and enforces it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, ClassVar, Final, get_args, get_origin

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo

__all__ = [
    "CredentialStorage",
    "FieldSpec",
    "Model",
    "Pending",
    "Relationship",
    "Rule",
    "UniqueTogether",
    "field",
]


# ---------------------------------------------------------------------------
# Logical types and markers
# ---------------------------------------------------------------------------

LOGICAL_TYPES: Final[dict[str, type]] = {
    "integer": int,
    "string": str,
    "boolean": bool,
    "decimal": Decimal,
    "float": float,
    "datetime": datetime,
}


class _Unset:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET: Final = _Unset()


class _Pending:
    """A value awaiting declared generation.

    It marks the absence of a value that the responsible technical Component
    must supply. It is never a placeholder: it holds no value, equals no
    value, and cannot be stored in place of one.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return "Pending"

    def __bool__(self) -> bool:
        return False


Pending: Final = _Pending()


# ---------------------------------------------------------------------------
# Fields
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FieldSpec:
    """The logical properties of one field, independent of any technology."""

    name: str
    type: str
    nullable: bool
    purpose: str | None
    primary_key: bool
    auto_increment: bool
    unique: bool
    credential: bool
    generated: bool
    size: int | None
    default: Any

    @property
    def has_default(self) -> bool:
        return self.default is not UNSET

    @property
    def assigned_by_storage(self) -> bool:
        """The storing layer assigns this field, so a caller may omit it."""
        return self.primary_key and self.auto_increment

    @property
    def python_type(self) -> type:
        return LOGICAL_TYPES[self.type]


def field(
    type: str,
    *,
    nullable: bool = False,
    purpose: str | None = None,
    primary_key: bool = False,
    auto_increment: bool = False,
    unique: bool = False,
    credential: bool = False,
    generated: bool = False,
    size: int | None = None,
    default: Any = UNSET,
) -> Any:
    """Declare one field with its logical properties.

    ``type`` is a logical type name: integer, string, boolean, decimal, float,
    or datetime. ``generated`` states that a value for this field may be
    supplied by declared generation rather than by a caller; only such a field
    accepts the ``Pending`` marker.
    """
    if type not in LOGICAL_TYPES:
        raise ValueError(f"unknown logical type {type!r}")
    spec = {
        "type": type,
        "nullable": nullable,
        "purpose": purpose,
        "primary_key": primary_key,
        "auto_increment": auto_increment,
        "unique": unique,
        "credential": credential,
        "generated": generated,
        "size": size,
        "default": None if default is UNSET else default,
        "has_default": default is not UNSET,
    }
    kwargs: dict[str, Any] = {"json_schema_extra": {"logical": spec}}
    if size is not None:
        kwargs["max_length"] = size
    if default is not UNSET:
        kwargs["default"] = default
    elif nullable or auto_increment:
        kwargs["default"] = None
    return Field(**kwargs)


def _spec_from(name: str, info: FieldInfo) -> FieldSpec:
    extra = info.json_schema_extra
    logical = extra["logical"] if isinstance(extra, dict) else None
    if logical is None:
        raise TypeError(f"field {name!r} was not declared with field()")
    return FieldSpec(
        name=name,
        type=logical["type"],
        nullable=logical["nullable"],
        purpose=logical["purpose"],
        primary_key=logical["primary_key"],
        auto_increment=logical["auto_increment"],
        unique=logical["unique"],
        credential=logical["credential"],
        generated=logical["generated"],
        size=logical["size"],
        default=logical["default"] if logical["has_default"] else UNSET,
    )


# ---------------------------------------------------------------------------
# Relationships and rules
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Relationship:
    """A conceptual connection to another Model, carried by one field.

    ``kind`` is ``belongs_to`` when the Model is contained by the target, and
    ``uses`` when it merely refers to the target.
    """

    field: str
    target: type[Model]
    kind: str = "belongs_to"
    role: str | None = None


@dataclass(frozen=True)
class UniqueTogether:
    """The combination of the named fields must be unique across records.

    It constrains stored state, so it is declared here and guaranteed by the
    Component that stores the Model.
    """

    fields: tuple[str, ...]


@dataclass(frozen=True)
class CredentialStorage:
    """A credential field must use the named storage mode at rest."""

    field: str
    mode: str


Rule = UniqueTogether | CredentialStorage


# ---------------------------------------------------------------------------
# Model base
# ---------------------------------------------------------------------------


class Model(BaseModel):
    """Base of every domain Model.

    Constructing a Model validates a complete domain state strictly: every
    field holds a value of its declared logical type, every required field is
    present, and no undeclared field is given. Use the package's validation
    support when a value may be absent, explicitly null, or awaiting declared
    generation, because those three are distinct and a constructor cannot
    tell them apart.
    """

    model_config = ConfigDict(strict=True, extra="forbid", validate_assignment=True)

    logical_name: ClassVar[str] = ""
    relationships: ClassVar[tuple[Relationship, ...]] = ()
    rules: ClassVar[tuple[Rule, ...]] = ()
    initial_data: ClassVar[tuple[dict[str, Any], ...]] = ()

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if not cls.logical_name:
            cls.logical_name = cls.__name__
        specs = cls.field_specs()
        for name, info in cls.model_fields.items():
            spec = specs[name]
            if _base_type(info.annotation) is not spec.python_type:
                raise TypeError(
                    f"{cls.__name__}.{name}: annotation {info.annotation!r} does not "
                    f"match logical type {spec.type!r}"
                )
        for rel in cls.relationships:
            if rel.field not in specs:
                raise TypeError(f"{cls.__name__}: relationship field {rel.field!r} is not declared")
        for rule in cls.rules:
            names = rule.fields if isinstance(rule, UniqueTogether) else (rule.field,)
            for name in names:
                if name not in specs:
                    raise TypeError(f"{cls.__name__}: rule field {name!r} is not declared")
            if isinstance(rule, CredentialStorage) and not specs[rule.field].credential:
                raise TypeError(f"{cls.__name__}: {rule.field!r} is not a credential field")
        for record in cls.initial_data:
            unknown = set(record) - set(specs)
            if unknown:
                raise TypeError(f"{cls.__name__}: initial data names unknown fields {sorted(unknown)}")
            for name, value in record.items():
                if value is Pending and not specs[name].generated:
                    raise TypeError(
                        f"{cls.__name__}: initial data awaits generation for {name!r}, "
                        f"which does not permit it"
                    )

    @classmethod
    def field_specs(cls) -> dict[str, FieldSpec]:
        """The logical properties of every field, in declaration order."""
        return {name: _spec_from(name, info) for name, info in cls.model_fields.items()}

    @classmethod
    def field_spec(cls, name: str) -> FieldSpec:
        return cls.field_specs()[name]


def _base_type(annotation: Any) -> Any:
    """Strip an optional wrapper from an annotation."""
    if get_origin(annotation) is not None:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation
