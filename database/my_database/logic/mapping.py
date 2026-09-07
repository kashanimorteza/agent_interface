"""The engine-independent storage design derived from the shared Models.

Every persistent Model maps to one table that records its source Model. Each
field becomes a column carrying the field's declared properties, and each
relationship an explicit foreign key whose optionality is the optionality the
Model itself resolves for the carrying field: this layer applies no separate
nullability default. Every Model rule whose truth depends on stored data
becomes a guarantee recorded against the rule it implements, and a credential
field resolves to one at-rest mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from my_model import MODELS, CredentialStorage, FieldSpec, Model, UniqueTogether
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

from ..errors import UnsupportedRequirement

# Resolved from Database Preferences: exact-name credential defaults and the
# selected default mode used when no field-specific default applies.
CREDENTIAL_FIELD_DEFAULTS: dict[str, str] = {"password": "hash", "api_key": "hash"}
CREDENTIAL_DEFAULT_MODE = "plaintext"
AT_REST_MODES = ("plaintext", "hash", "encrypted")

# Physical mapping choices this layer supplies where the Model states none.
DECIMAL_PRECISION = 28
DECIMAL_SCALE = 10
REFERENTIAL_ACTION = "RESTRICT"

# What each kind of guarantee needs from an Engine to be enforced at commit.
ENGINE_REQUIREMENTS = {
    "unique": "unique constraint",
    "unique_together": "composite unique constraint",
    "reference": "foreign key constraint",
}


def pluralize(word: str) -> str:
    if word.endswith("y") and word[-2:-1] not in "aeiou":
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"


def snake_case(name: str) -> str:
    out = []
    for i, ch in enumerate(name):
        if ch.isupper() and i and (not name[i - 1].isupper() or (i + 1 < len(name) and name[i + 1].islower())):
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


def table_name(model: type[Model]) -> str:
    """plural_snake_case of the Model's name."""
    return pluralize(snake_case(model.__name__))


def column_type(spec: FieldSpec) -> Any:
    match spec.type:
        case "integer":
            return Integer()
        case "string":
            return String(spec.size) if spec.size else String()
        case "boolean":
            return Boolean()
        case "decimal":
            return Numeric(DECIMAL_PRECISION, DECIMAL_SCALE, asdecimal=True)
        case "float":
            return Float()
        case "datetime":
            return DateTime()
    raise ValueError(f"unknown logical type {spec.type!r}")


@dataclass(frozen=True)
class ColumnMapping:
    field: str
    column: str
    type: str
    nullable: bool
    unique: bool
    primary_key: bool
    assigned_by_storage: bool
    size: int | None
    default: Any
    has_default: bool
    credential: bool


@dataclass(frozen=True)
class ForeignKeyMapping:
    model: type[Model]
    field: str
    kind: str
    role: str | None
    referenced_model: type[Model]
    referenced_table: str
    referenced_column: str
    nullable: bool
    index: str
    on_delete: str
    on_update: str


@dataclass(frozen=True)
class Guarantee:
    """One rule over stored data that this layer enforces when changes commit."""

    model: type[Model]
    kind: str
    name: str
    fields: tuple[str, ...]
    source: str
    source_rule: Any = None
    detail: str | None = None


@dataclass(frozen=True)
class TableMapping:
    model: type[Model]
    table: Table
    columns: dict[str, ColumnMapping]
    foreign_keys: tuple[ForeignKeyMapping, ...]
    guarantees: tuple[Guarantee, ...]
    at_rest: dict[str, str]

    @property
    def name(self) -> str:
        return self.table.name

    @property
    def identifier(self) -> str:
        return next(c.field for c in self.columns.values() if c.primary_key)


def resolve_at_rest(model: type[Model]) -> dict[str, str]:
    """The at-rest mode of every credential field.

    An explicit rule takes precedence, then the exact-name default, then the
    selected default mode.
    """
    explicit = {r.field: r.mode for r in model.rules if isinstance(r, CredentialStorage)}
    modes: dict[str, str] = {}
    for name, spec in model.field_specs().items():
        if not spec.credential:
            continue
        mode = explicit.get(name) or CREDENTIAL_FIELD_DEFAULTS.get(name) or CREDENTIAL_DEFAULT_MODE
        if mode not in AT_REST_MODES:
            raise ValueError(f"{model.__name__}.{name}: unknown at-rest mode {mode!r}")
        modes[name] = mode
    return modes


class StorageMapping:
    """The complete derived storage design for a set of Models."""

    def __init__(self, models: tuple[type[Model], ...] = MODELS, *, engine: str = "SQLite") -> None:
        self.metadata = MetaData()
        self.models = models
        self.engine = engine
        self.tables: dict[type[Model], TableMapping] = {}
        for model in models:  # project order is dependency order
            self.tables[model] = self._build(model)
        self._require_enforceable()

    def for_model(self, model: type[Model]) -> TableMapping:
        try:
            return self.tables[model]
        except KeyError:
            raise KeyError(f"{model!r} is not a mapped Model") from None

    @property
    def guarantees(self) -> tuple[Guarantee, ...]:
        return tuple(g for tm in self.tables.values() for g in tm.guarantees)

    def _require_enforceable(self) -> None:
        """No guarantee within this layer's responsibility is silently dropped."""
        for guarantee in self.guarantees:
            if guarantee.kind not in ENGINE_REQUIREMENTS:
                raise UnsupportedRequirement(
                    f"{guarantee.model.__name__}: {guarantee.name} needs an enforcement "
                    f"the {self.engine} Engine does not provide"
                )

    def _build(self, model: type[Model]) -> TableMapping:
        name = table_name(model)
        specs = model.field_specs()
        at_rest = resolve_at_rest(model)
        relationships = {r.field: r for r in model.relationships}
        columns: list[Column] = []
        column_maps: dict[str, ColumnMapping] = {}
        fk_maps: list[ForeignKeyMapping] = []
        guarantees: list[Guarantee] = []

        for field_name, spec in specs.items():
            args: list[Any] = [field_name, column_type(spec)]
            kwargs: dict[str, Any] = {
                # optionality comes from the resolved Model field, here and for
                # a relationship field; this layer adds no default of its own.
                "nullable": spec.nullable,
                "unique": spec.unique or None,
                "primary_key": spec.primary_key,
                "autoincrement": spec.auto_increment,
                "comment": f"{model.__name__}.{field_name}",
            }
            if spec.has_default:
                kwargs["default"] = spec.default
            relationship = relationships.get(field_name)
            if relationship is not None:
                target = self.tables[relationship.target]
                referenced = target.identifier
                args.append(
                    ForeignKey(
                        f"{target.name}.{referenced}",
                        name=f"fk_{name}_{field_name}",
                        ondelete=REFERENTIAL_ACTION,
                        onupdate=REFERENTIAL_ACTION,
                    )
                )
                kwargs["index"] = True
                fk_maps.append(
                    ForeignKeyMapping(
                        model=model,
                        field=field_name,
                        kind=relationship.kind,
                        role=relationship.role,
                        referenced_model=relationship.target,
                        referenced_table=target.name,
                        referenced_column=referenced,
                        nullable=spec.nullable,
                        index=f"ix_{name}_{field_name}",
                        on_delete=REFERENTIAL_ACTION,
                        on_update=REFERENTIAL_ACTION,
                    )
                )
                guarantees.append(Guarantee(
                    model=model,
                    kind="reference",
                    name=f"fk_{name}_{field_name}",
                    fields=(field_name,),
                    source=f"{model.__name__}.relationships[{field_name}]",
                    source_rule=relationship,
                    detail=f"{target.name}.{referenced} must hold the referenced record",
                ))
            columns.append(Column(*args, **kwargs))
            column_maps[field_name] = ColumnMapping(
                field=field_name,
                column=field_name,
                type=spec.type,
                nullable=spec.nullable,
                unique=spec.unique,
                primary_key=spec.primary_key,
                assigned_by_storage=spec.assigned_by_storage,
                size=spec.size,
                default=spec.default if spec.has_default else None,
                has_default=spec.has_default,
                credential=spec.credential,
            )
            if spec.unique:
                guarantees.append(Guarantee(
                    model=model,
                    kind="unique",
                    name=f"uq_{name}_{field_name}",
                    fields=(field_name,),
                    source=f"{model.__name__}.{field_name}.unique",
                ))

        table_args: list[Any] = list(columns)
        for rule in model.rules:
            if isinstance(rule, UniqueTogether):
                constraint = f"uq_{name}_{'_'.join(rule.fields)}"
                table_args.append(UniqueConstraint(*rule.fields, name=constraint))
                guarantees.append(Guarantee(
                    model=model,
                    kind="unique_together",
                    name=constraint,
                    fields=rule.fields,
                    source=f"{model.__name__}.rules",
                    source_rule=rule,
                ))
        table = Table(name, self.metadata, *table_args, comment=f"source model: {model.__name__}")
        return TableMapping(model, table, column_maps, tuple(fk_maps), tuple(guarantees), at_rest)
