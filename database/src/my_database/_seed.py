"""Seeds every Model's declared initial data, in dependency order, repeatably."""

from __future__ import annotations

import my_model as m

from . import _operations, _relationships, _secrets


def _lookup_keys(model_cls: type, record: dict) -> dict:
    """The fields that identify this declared record among stored rows."""
    for group in getattr(model_cls, "unique_together", ()):
        if all(k in record for k in group):
            return {k: record[k] for k in group}
    for name, info in model_cls.model_fields.items():
        extra = info.json_schema_extra if isinstance(info.json_schema_extra, dict) else {}
        if extra.get("unique") and name in record:
            return {name: record[name]}
    credential_fields = set(model_cls.credential_fields())
    return {k: v for k, v in record.items() if k not in credential_fields}


def seed_all(instance: str | None = None) -> dict[str, int]:
    """Seeds every declared initial record. Returns the count inserted per Model."""
    inserted: dict[str, int] = {}
    with _operations.transaction(instance) as conn:
        for model_cls in _relationships.PERSISTENT_MODELS:
            records = m.INITIAL_DATA.get(model_cls, ())
            count = 0
            for record in records:
                resolved = {
                    k: (_secrets.generate_secure_value() if v is m.GENERATE_SECURELY else v)
                    for k, v in record.items()
                }
                keys = _lookup_keys(model_cls, resolved)
                existing = _operations.list_(model_cls, conn=conn, **keys)
                if existing:
                    continue
                _operations.create(model_cls, conn=conn, **resolved)
                count += 1
            if count:
                inserted[model_cls.__name__] = count
    return inserted
