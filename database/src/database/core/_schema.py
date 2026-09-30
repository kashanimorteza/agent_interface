"""Derivation of stored structure from the public Entity Declarations.

The structure (tables, keys, Relations, Uniqueness Constraints, Indexes) is the same
for every Instance. Each Instance supplies only its own column types.
"""

import hashlib
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    MetaData,
    Table,
    UniqueConstraint,
    false,
    text,
    true,
)
from sqlalchemy.sql.elements import ColumnElement, TextClause
from sqlalchemy.types import TypeEngine

from database.core._failures import DeclarationFailure

_IDENTIFIER_LIMIT = 63

type ColumnType = Callable[[Any], TypeEngine[Any]]


@dataclass(frozen=True, slots=True)
class Schema:
    """The stored structure of every public Entity on one Instance."""

    metadata: MetaData
    tables: Mapping[str, Table]
    declarations: Mapping[str, Any]

    def column(self, entity: str, field: str) -> Column[Any]:
        return self.tables[entity].c[field]


def _snake(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _plural(word: str) -> str:
    if word.endswith("y") and word[-2] not in "aeiou":
        return word[:-1] + "ies"
    return word + "s"


def _bounded(name: str) -> str:
    if len(name) <= _IDENTIFIER_LIMIT:
        return name
    digest = hashlib.sha256(name.encode()).hexdigest()[:8]
    return f"{name[: _IDENTIFIER_LIMIT - 9]}_{digest}"


def _server_default(declared: Any) -> ColumnElement[Any] | TextClause | None:
    if not declared.has_default or declared.default is None:
        return None
    value = declared.default
    if isinstance(value, bool):
        return true() if value else false()
    if isinstance(value, (int, float, Decimal)):
        return text(str(value))
    if isinstance(value, str):
        return text("'" + value.replace("'", "''") + "'")
    return None


def build_schema(declarations: Mapping[str, Any], column_type: ColumnType) -> Schema:
    """Derive the tables, constraints, and indexes of every public Entity."""
    metadata = MetaData()
    table_names = {
        identity: _plural(_snake(declaration.name))
        for identity, declaration in declarations.items()
    }
    by_logical = {
        declaration.name: identity for identity, declaration in declarations.items()
    }
    tables: dict[str, Table] = {}
    for identity, declaration in declarations.items():
        name = table_names[identity]
        relations = {
            relation.local_field: relation for relation in declaration.relations
        }
        columns: list[Column[Any] | ForeignKey | UniqueConstraint | Index] = []
        for declared in declaration.fields:
            arguments: list[Any] = [declared.name, column_type(declared)]
            if declared.name in relations:
                relation = relations[declared.name]
                target = by_logical.get(relation.target_entity)
                if target is None:
                    raise DeclarationFailure(
                        f"Entity {declaration.name} relates an unknown Entity."
                    )
                arguments.append(
                    ForeignKey(
                        f"{table_names[target]}.{relation.target_field}",
                        name=_bounded(f"fk_{name}_{declared.name}"),
                    )
                )
            is_key = declared.name == declaration.primary_key
            columns.append(
                Column(
                    *arguments,
                    nullable=declared.nullable and not is_key,
                    primary_key=is_key,
                    autoincrement=declared.value_generation == "auto_increment",
                    server_default=_server_default(declared),
                )
            )
        for group in declaration.unique_constraints:
            columns.append(
                UniqueConstraint(*group, name=_bounded(f"uq_{name}_{'_'.join(group)}"))
            )
        for group in declaration.indexes:
            columns.append(Index(_bounded(f"ix_{name}_{'_'.join(group)}"), *group))
        tables[identity] = Table(name, metadata, *columns)
    return Schema(metadata, tables, dict(declarations))
