"""Seeding of the initial data every Model declares.

Records are applied in dependency order, explicit relationship identifiers
are preserved, generated values are produced once and stored only in their
at-rest form, and a record that already exists is skipped so that seeding is
repeatable.
"""

from __future__ import annotations

import secrets as _secrets
from dataclasses import dataclass, field
from typing import Any

from my_model import Generate, Model, UniqueTogether
from sqlalchemy import insert, select

from ..adapter.connection import StorageAdapter
from ..errors import InvalidOperation
from .credentials import CredentialTransformer
from .mapping import StorageMapping, TableMapping

GENERATED_LENGTH = 24


@dataclass(frozen=True)
class GeneratedSecret:
    """A secret generated during seeding, reported once and never stored as given."""

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
    """Field sets that identify a record: each unique field present, then each
    composite uniqueness rule whose fields are all present."""
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
    def __init__(self, mapping: StorageMapping, adapter: StorageAdapter, credentials: CredentialTransformer) -> None:
        self.mapping = mapping
        self.adapter = adapter
        self.credentials = credentials

    def seed(self, instance: str | None = None) -> SeedReport:
        report = SeedReport()
        with self.adapter.connect(instance) as conn:
            for model in self.mapping.models:  # project order is dependency order
                tm = self.mapping.for_model(model)
                for raw in model.initial_data:
                    record = dict(raw)
                    if self._exists(conn, tm, record):
                        report.skipped[model.__name__] = report.skipped.get(model.__name__, 0) + 1
                        continue
                    stored = self._prepare(tm, record, report)
                    conn.execute(insert(tm.table).values(**stored))
                    report.inserted[model.__name__] = report.inserted.get(model.__name__, 0) + 1
        return report

    def _exists(self, conn, tm: TableMapping, record: dict[str, Any]) -> bool:
        keys = identity_keys(tm.model, record)
        if not keys:
            return False
        for fields in keys:
            stmt = select(tm.table.c[tm.primary_key])
            for f in fields:
                stmt = stmt.where(tm.table.c[f] == record[f])
            if conn.execute(stmt).first() is not None:
                return True
        return False

    def _prepare(self, tm: TableMapping, record: dict[str, Any], report: SeedReport) -> dict[str, Any]:
        specs = tm.model.field_specs()
        label = record_label(record)
        values: dict[str, Any] = {}
        for name, value in record.items():
            if value is Generate:
                value = _secrets.token_urlsafe(GENERATED_LENGTH)
                report.generated.append(GeneratedSecret(tm.model.__name__, label, name, value))
            values[name] = value
        # validate against the Model with defaults applied before storing
        validated = tm.model.model_validate(values).model_dump()
        if validated.get(tm.primary_key) is None:
            validated.pop(tm.primary_key, None)
        for name, mode in tm.at_rest.items():
            if name in validated and validated[name] is not None:
                validated[name] = self.credentials.transform(mode, validated[name])
        for name in validated:
            if name not in specs:
                raise InvalidOperation(f"{tm.model.__name__}: initial data names unknown field {name!r}")
        return validated
