"""Seeding of the initial data every Model declares.

Records are applied in dependency order, explicit relationship identifiers
are preserved, the values a record leaves awaiting generation are produced
here and stored only in their at-rest form, and a record that already exists
is skipped so that seeding is repeatable.
"""

from __future__ import annotations

import secrets as _secrets
from dataclasses import dataclass, field
from typing import Any

from my_model import Model, UniqueTogether, validate_state
from sqlalchemy import Connection, insert, select

from .credentials import CredentialTransformer
from .mapping import StorageMapping, TableMapping

GENERATED_LENGTH = 24


@dataclass(frozen=True)
class GeneratedSecret:
    """A secret produced during seeding, reported once and stored only at rest."""

    model: str
    record: str
    field: str
    value: str


@dataclass
class SeedReport:
    inserted: dict[str, int] = field(default_factory=dict)
    skipped: dict[str, int] = field(default_factory=dict)
    generated: list[GeneratedSecret] = field(default_factory=list)


def identity_keys(model: type[Model], record: dict[str, Any]) -> list[tuple[str, ...]]:
    """Field sets that identify a record already present."""
    keys: list[tuple[str, ...]] = []
    for name, spec in model.field_specs().items():
        if spec.unique and name in record:
            keys.append((name,))
    for rule in model.rules:
        if isinstance(rule, UniqueTogether) and all(f in record for f in rule.fields):
            keys.append(rule.fields)
    return keys


def record_label(record: dict[str, Any]) -> str:
    for candidate in ("name", "code", "symbol", "username"):
        if candidate in record:
            return str(record[candidate])
    return repr(record)


class Seeder:
    def __init__(self, mapping: StorageMapping, credentials: CredentialTransformer) -> None:
        self.mapping = mapping
        self.credentials = credentials

    def seed(self, connection: Connection) -> SeedReport:
        """Apply every declared record that is not already present."""
        report = SeedReport()
        for model in self.mapping.models:  # project order is dependency order
            tm = self.mapping.for_model(model)
            for declared in model.initial_data:
                record = dict(declared)
                if self._exists(connection, tm, record):
                    report.skipped[model.__name__] = report.skipped.get(model.__name__, 0) + 1
                    continue
                values = self._prepare(tm, record, report)
                connection.execute(insert(tm.table).values(**values))
                report.inserted[model.__name__] = report.inserted.get(model.__name__, 0) + 1
        return report

    def _exists(self, connection: Connection, tm: TableMapping, record: dict[str, Any]) -> bool:
        for fields in identity_keys(tm.model, record):
            statement = select(tm.table.c[tm.identifier])
            for name in fields:
                statement = statement.where(tm.table.c[name] == record[name])
            if connection.execute(statement).first() is not None:
                return True
        return False

    def _prepare(self, tm: TableMapping, record: dict[str, Any], report: SeedReport) -> dict[str, Any]:
        """The stored values for one declared record, generation resolved."""
        label = record_label(record)
        state = validate_state(tm.model, record)
        generated = {}
        for name in sorted(state.pending):
            value = _secrets.token_urlsafe(GENERATED_LENGTH)
            generated[name] = value
            report.generated.append(GeneratedSecret(tm.model.__name__, label, name, value))
        values = state.resolved(**generated).model_dump()
        if values.get(tm.identifier) is None:
            values.pop(tm.identifier, None)
        for name, mode in tm.at_rest.items():
            if values.get(name) is not None:
                values[name] = self.credentials.transform(mode, values[name])
        return values
