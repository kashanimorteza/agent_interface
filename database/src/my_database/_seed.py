from __future__ import annotations

import re

import my_model
from my_model import DomainModel

from ._gateway import Database
from ._schema import TABLE_NAMES

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


def _initial_data_constant_name(model_cls: type[DomainModel]) -> str:
    snake = _CAMEL_BOUNDARY.sub("_", model_cls.__name__).upper()
    return f"{snake}_INITIAL_DATA"


SEED_ORDER: list[type[DomainModel]] = [
    model_cls
    for model_cls in TABLE_NAMES
    if hasattr(my_model, _initial_data_constant_name(model_cls))
]


def _natural_key(model_cls: type[DomainModel], record: dict) -> dict:
    if model_cls.unique_fields and model_cls.unique_fields.issubset(record):
        fields = model_cls.unique_fields
    elif model_cls.unique_together and set(model_cls.unique_together[0]).issubset(record):
        fields = set(model_cls.unique_together[0])
    else:
        fields = set(record)
    return {f: record[f] for f in fields}


def seed_all(db: Database | None = None) -> dict[str, int]:
    db = db or Database()
    inserted = {}
    for model_cls in SEED_ORDER:
        records = getattr(my_model, _initial_data_constant_name(model_cls))
        count = 0
        for record in records:
            key = _natural_key(model_cls, record)
            if db.list(model_cls, where=key):
                continue
            db.create(model_cls, record)
            count += 1
        inserted[model_cls.__name__] = count
    return inserted
