"""The generic Model-to-storage mapping mechanism.

Derives each persistent Domain Definition's physical storage structure
directly from the technology-independent persistence metadata Model
publishes for it (``persistence_contract()``), and classifies every
persistence decision as portable contract, portable mapping, or an
isolated, recorded Engine-specific extension.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from model import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    ModelBase,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from pydantic import AwareDatetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
)

PERSISTENT_MODELS: tuple[type[ModelBase], ...] = (
    User,
    TradingPlatform,
    Instance,
    Currency,
    Broker,
    Asset,
    AccountGroup,
    Account,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)


def camel_to_snake(name: str) -> str:
    """Convert a PascalCase Domain Definition name to its snake_case model key."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def pluralize(word: str) -> str:
    """Pluralize a snake_case model key into the plural_snake_case table-naming convention."""
    if word.endswith("y") and (len(word) < 2 or word[-2] not in "aeiou"):
        return word[:-1] + "ies"
    return word + "s"


MODEL_KEYS: dict[str, type[ModelBase]] = {
    camel_to_snake(m.__name__): m for m in PERSISTENT_MODELS
}


def model_key(model_cls: type[ModelBase]) -> str:
    """The snake_case key a foreign_key reference or the model registry addresses this Domain Definition by."""
    return camel_to_snake(model_cls.__name__)


def table_name(model_cls: type[ModelBase]) -> str:
    """The plural_snake_case physical table name for a Domain Definition."""
    return pluralize(model_key(model_cls))


@dataclass(frozen=True)
class PortabilityNote:
    """One persistence decision, classified for Database portability transparency."""

    subject: str
    classification: str
    note: str


PORTABILITY_LEDGER: tuple[PortabilityNote, ...] = (
    PortabilityNote(
        subject="Field identity, uniqueness, nullability, defaults, foreign keys, relationship cardinality",
        classification="portable_contract",
        note="Derived directly from each Domain Definition's persistence_contract(); holds for any relational Engine.",
    ),
    PortabilityNote(
        subject="Table, column, and index naming (plural_snake_case tables, snake_case columns, ix_<table>_<column> indexes)",
        classification="portable_mapping",
        note="A physical naming convention applied consistently; changing it does not change portable meaning.",
    ),
    PortabilityNote(
        subject="Decimal column precision and scale (18, 8)",
        classification="portable_mapping",
        note="A project-chosen physical precision/scale for exact-value fields; Numeric itself is supported across relational Engines.",
    ),
    PortabilityNote(
        subject="SQLite foreign-key enforcement (`PRAGMA foreign_keys = ON` per connection)",
        classification="engine_specific_extension",
        note=(
            "SQLite does not enforce declared foreign keys unless this pragma is set per connection; "
            "a server Engine such as PostgreSQL or MySQL enforces them natively and needs no such pragma. "
            "Isolated in the Storage Adapter's connection setup."
        ),
    ),
    PortabilityNote(
        subject="SQLite single-writer connection handling (`check_same_thread=False` with a serialized pool)",
        classification="engine_specific_extension",
        note=(
            "Required only for SQLite's file-based, single-writer connection model; a server Engine's driver "
            "handles concurrent connections natively. Isolated in the Storage Adapter."
        ),
    ),
    PortabilityNote(
        subject="Concurrent Migration run coordination",
        classification="engine_specific_extension",
        note=(
            "SQLite serializes concurrent writers, Migration runs included, through the operating system's "
            "file lock on the database file; a server Engine instead needs its own advisory or session lock, "
            "isolated in database.migrations if a server Engine is added."
        ),
    ),
)


def portability_report() -> tuple[PortabilityNote, ...]:
    """Publish this mapping mechanism's recorded portability classification of its persistence decisions."""
    return PORTABILITY_LEDGER


def _column_type(annotation: Any) -> Any:
    args = [
        a for a in getattr(annotation, "__args__", [annotation]) if a is not type(None)
    ]
    python_type = args[0] if args else annotation
    if python_type is int:
        return Integer()
    if python_type is str:
        return String()
    if python_type is bool:
        return Boolean()
    if python_type is float:
        return Float()
    if python_type is Decimal:
        return Numeric(precision=18, scale=8)
    if python_type in (datetime, AwareDatetime):
        return DateTime(timezone=True)
    msg = f"No portable column type mapping for annotation {annotation!r}"
    raise TypeError(msg)


def build_table(model_cls: type[ModelBase], metadata: MetaData) -> Table:
    """Derive one SQLAlchemy Table from a persistent Domain Definition's published persistence contract."""
    contract = model_cls.persistence_contract()
    tname = table_name(model_cls)
    columns: list[Column[Any]] = []
    for field_name, field_meta in contract["fields"].items():
        annotation = model_cls.model_fields[field_name].annotation
        col_args: list[Any] = []
        if "foreign_key" in field_meta:
            ref_key, ref_column = field_meta["foreign_key"].split(".")
            ref_table = table_name(MODEL_KEYS[ref_key])
            col_args.append(ForeignKey(f"{ref_table}.{ref_column}"))
        columns.append(
            Column(
                field_name,
                _column_type(annotation),
                *col_args,
                primary_key=bool(field_meta["primary_key"]),
                autoincrement=bool(field_meta["auto_increment"]),
                unique=bool(field_meta["unique"]) and not field_meta["primary_key"],
                nullable=bool(field_meta["nullable"]),
            )
        )

    table_args: list[Any] = []
    for unique_set in contract["unique_sets"]:
        table_args.append(
            UniqueConstraint(*unique_set, name=f"uq_{tname}_{'_'.join(unique_set)}")
        )
    for field_name, field_meta in contract["fields"].items():
        if field_meta.get("index") and not field_meta["primary_key"]:
            table_args.append(Index(f"ix_{tname}_{field_name}", field_name))

    return Table(tname, metadata, *columns, *table_args)


def build_metadata() -> MetaData:
    """Build one MetaData containing every persistent Domain Definition's derived Table."""
    metadata = MetaData()
    for model_cls in PERSISTENT_MODELS:
        build_table(model_cls, metadata)
    return metadata
