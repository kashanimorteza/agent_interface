"""The standard Model Logic baseline: create, get, list, update, and delete for one shared Model.

Independent of HTTP, the API framework, and the persistence technology. It depends only on the shared
Model specification, the Data Access boundary, and the Backend error types.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, ClassVar

from trading_backend.errors import InvalidFieldError, NotFoundError
from trading_backend.logic.model_specs import ModelSpec, get_spec


class ModelLogic:
    """Baseline logical unit of one shared Model; subclasses set ``model`` to their Model key."""

    model: ClassVar[str]

    def __init__(self, data_access: Any) -> None:
        self._data_access = data_access
        self._spec: ModelSpec = get_spec(self.model)

    # ------------------------------------------------------------ validation against the shared specification

    def _validate_write(self, data: Mapping[str, Any], *, partial: bool) -> dict[str, Any]:
        spec = self._spec
        unknown = [name for name in data if spec.field(name) is None]
        if unknown:
            raise InvalidFieldError(f"{spec.key} has no field {', '.join(map(repr, unknown))}")
        if spec.primary_key in data:
            raise InvalidFieldError(f"the primary key {spec.primary_key!r} of {spec.key} is generated and may not be supplied")
        if partial:
            for name, value in data.items():
                if value is None and not spec.field(name).nullable:
                    raise InvalidFieldError(f"field {name!r} of {spec.key} cannot be set to null")
        return dict(data)

    def _validate_order_by(self, order_by: Sequence[str] | None) -> list[str] | None:
        if order_by is None:
            return None
        checked: list[str] = []
        for entry in order_by:
            name = entry[1:] if entry.startswith("-") else entry
            field = self._spec.field(name)
            if field is None:
                raise InvalidFieldError(f"{self._spec.key} has no field {name!r} to order by")
            if field.credential:
                raise InvalidFieldError(f"credential field {name!r} of {self._spec.key} cannot be used for ordering")
            checked.append(entry)
        return checked

    # ------------------------------------------------------------ standard operations

    def create(self, data: Mapping[str, Any]) -> dict[str, Any]:
        """Create one record; Database applies the resolved defaults and credential transformations."""
        return self._data_access.create(self.model, self._validate_write(data, partial=False))

    def get(self, record_id: Any) -> dict[str, Any]:
        """One record by primary key; NotFoundError when absent."""
        record = self._data_access.read(self.model, record_id)
        if record is None:
            raise NotFoundError(f"{self.model} {record_id!r} does not exist")
        return record

    def list(
        self, *, order_by: Sequence[str] | None = None, limit: int | None = None, offset: int | None = None
    ) -> list[dict[str, Any]]:
        """Records ordered by ``order_by`` (leading '-' means descending) and paged."""
        return self._data_access.list(self.model, order_by=self._validate_order_by(order_by), limit=limit, offset=offset)

    def update(self, record_id: Any, data: Mapping[str, Any]) -> dict[str, Any]:
        """Apply a partial update to one record."""
        return self._data_access.update(self.model, record_id, self._validate_write(data, partial=True))

    def delete(self, record_id: Any) -> None:
        """Remove one record; a referenced record raises ConflictError from Data Access."""
        self._data_access.delete(self.model, record_id)
