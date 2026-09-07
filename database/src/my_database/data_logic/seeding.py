"""Idempotent application of declared initial data.

Records are applied in the order given, matched on their Model's natural key so
that re-running creates no duplicate; explicit relationship identifiers are
preserved; a ``GENERATE`` value is fulfilled with a cryptographically random
value at seed time; credential fields are stored through their at-rest mode.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy import and_, delete, insert, select
from sqlalchemy.engine import Connection

from . import credentials
from .mapping import mapped

GENERATE = "generate"
Notify = Callable[[str], None]


@dataclass(frozen=True)
class Seed:
    """The initial records of one Model and the natural key they are matched on."""

    model: type
    natural_key: tuple[str, ...]
    records: tuple[dict[str, Any], ...]


def requires_key(seeds: tuple[Seed, ...]) -> bool:
    """Whether applying the seeds writes an encrypted credential."""
    return any(
        mode == "encrypted" and any(field in record for record in seed.records)
        for seed in seeds
        for field, mode in mapped(seed.model).credentials.items()
    )


def apply(connection: Connection, seeds: tuple[Seed, ...], key: credentials.KeyProvider, notify: Notify | None = None) -> int:
    """Insert every record whose natural key is absent; returns the number inserted."""
    inserted = 0
    for seed in seeds:
        m = mapped(seed.model)
        table = m.table
        for record in seed.records:
            match = and_(*(table.c[f] == record[f] for f in seed.natural_key))
            if connection.execute(select(table.c.id).where(match)).first() is not None:
                continue
            values = dict(record)
            for field_name, value in list(values.items()):
                if value == GENERATE:
                    values[field_name] = credentials.generate_credential()
                    if notify is not None:
                        notify(f"{seed.model.__name__} {dict((f, record[f]) for f in seed.natural_key)} {field_name}: {values[field_name]}")
            instance = seed.model(**values)
            row = instance.model_dump(exclude={"id"})
            for field_name, mode in m.credentials.items():
                row[field_name] = credentials.transform(mode, row[field_name], key)
            connection.execute(insert(table).values(**row))
            inserted += 1
    return inserted


def remove(connection: Connection, seeds: tuple[Seed, ...]) -> int:
    """Delete the records matching the seeds' natural keys, last Model first."""
    removed = 0
    for seed in reversed(seeds):
        table = mapped(seed.model).table
        for record in reversed(seed.records):
            match = and_(*(table.c[f] == record[f] for f in seed.natural_key))
            removed += connection.execute(delete(table).where(match)).rowcount
    return removed
