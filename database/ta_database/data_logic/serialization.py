"""Convert mapped instances into plain records that never carry credential columns."""

from __future__ import annotations

from typing import Any

from ta_database.storage_adapter.credentials.transform import INFO_KEY


def to_record(instance: Any) -> dict[str, Any]:
    table = instance.__table__
    return {c.name: getattr(instance, c.name) for c in table.columns if INFO_KEY not in c.info}
