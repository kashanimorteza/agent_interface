"""The engine-independent storage design derived from the shared Models.

Every persistent Model maps to one table that records its source Model. Each
field becomes a column carrying the field's declared properties, each
relationship an explicit foreign key, each rule a constraint traceable to it,
and each credential field a resolved at-rest mode.
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

# Resolved from Database Preferences: exact-name credential defaults and the
# selected default at-rest mode used when no field-specific default applies.
CREDENTIAL_FIELD_DEFAULTS: dict[str, str] = {"password": "hash", "api_key": "hash"}
CREDENTIAL_DEFAULT_MODE = "plaintext"
AT_REST_MODES = ("plaintext", "hash", "encrypted")

# Decimal fields carry no precision in the Model; this is the storage default.
DECIMAL_PRECISION = 28
DECIMAL_SCALE = 10

REFERENTIAL_ACTION = "RESTRICT"


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
    """plural_snake_case of the Model's class name."""
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
    auto_increment: bool
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
    index: str
    on_delete: str
    on_update: str


@dataclass(frozen=True)
class ConstraintMapping:
    model: type[Model]
    name: str
    kind: str  # "unique_together" | "at_rest"
    fields: tuple[str, ...]
    source_rule: Any
    detail: str | None = None


@dataclass(frozen=True)
class TableMapping:
    model: type[Model]
    table: Table
    columns: dict[str, ColumnMapping]
    foreign_keys: tuple[ForeignKeyMapping, ...]
    constraints: tuple[ConstraintMapping, ...]
    at_rest: dict[str, str]

    @property
    def name(self) -> str:
        return self.table.name

    @property
    def primary_key(self) -> str:
        return next(c.field for c in self.columns.values() if c.primary_key)


def resolve_at_rest(model: type[Model]) -> dict[str, str]:
    """The at-rest mode of every credential field: explicit rule first, then
    the exact-name default, then the selected default mode."""
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

    def __init__(self, models: tuple[type[Model], ...] = MODELS) -> None:
        self.metadata = MetaData()
        self.models = models
        self.tables: dict[type[Model], TableMapping] = {}
        for model in models:  # project order is dependency order
            self.tables[model] = self._build(model)

    def for_model(self, model: type[Model]) -> TableMapping:
        try:
            return self.tables[model]
        except KeyError:
            raise KeyError(f"{model!r} is not a mapped Model") from None

    def _build(self, model: type[Model]) -> TableMapping:
        name = table_name(model)
        specs = model.field_specs()
        at_rest = resolve_at_rest(model)
        relationships = {r.field: r for r in model.relationships}
        columns: list[Column] = []
        column_maps: dict[str, ColumnMapping] = {}
        fk_maps: list[ForeignKeyMapping] = []
        constraint_maps: list[ConstraintMapping] = []

        for field_name, spec in specs.items():
            args: list[Any] = [field_name, column_type(spec)]
            kwargs: dict[str, Any] = {
                "nullable": spec.nullable,
                "unique": spec.unique or None,
                "primary_key": spec.primary_key,
                "autoincrement": spec.auto_increment,
                "comment": f"{model.__name__}.{field_name}",
            }
            if spec.has_default:
                kwargs["default"] = spec.default
            rel = relationships.get(field_name)
            if rel is not None:
                target = self.tables[rel.target]
                ref_col = target.primary_key
                args.append(
                    ForeignKey(
                        f"{target.name}.{ref_col}",
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
                        kind=rel.kind,
                        role=rel.role,
                        referenced_model=rel.target,
                        referenced_table=target.name,
                        referenced_column=ref_col,
                        index=f"ix_{name}_{field_name}",
                        on_delete=REFERENTIAL_ACTION,
                        on_update=REFERENTIAL_ACTION,
                    )
                )
            columns.append(Column(*args, **kwargs))
            column_maps[field_name] = ColumnMapping(
                field=field_name,
                column=field_name,
                type=spec.type,
                nullable=spec.nullable,
                unique=spec.unique,
                primary_key=spec.primary_key,
                auto_increment=spec.auto_increment,
                size=spec.size,
                default=spec.default if spec.has_default else None,
                has_default=spec.has_default,
                credential=spec.credential,
            )

        table_args: list[Any] = list(columns)
        for rule in model.rules:
            if isinstance(rule, UniqueTogether):
                cname = f"uq_{name}_{'_'.join(rule.fields)}"
                table_args.append(UniqueConstraint(*rule.fields, name=cname))
                constraint_maps.append(ConstraintMapping(model, cname, "unique_together", rule.fields, rule))
            elif isinstance(rule, CredentialStorage):
                constraint_maps.append(
                    ConstraintMapping(model, f"at_rest_{name}_{rule.field}", "at_rest", (rule.field,), rule, at_rest[rule.field])
                )
        table = Table(name, self.metadata, *table_args, comment=f"source model: {model.__name__}")
        return TableMapping(model, table, column_maps, tuple(fk_maps), tuple(constraint_maps), at_rest)
