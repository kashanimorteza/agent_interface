"""The shared, reusable Logic baseline every Model's Logic unit builds on."""

from __future__ import annotations

from typing import ClassVar, Literal, cast

import my_model as m

from .. import data_access


class ModelLogic[ModelT: m.BaseModel]:
    """Common create/get/list/update/delete/status Behaviour for one Model.

    Every Model receives its own subclass (even when, as here, it currently
    needs nothing beyond this baseline) so Model-specific Behaviour can be
    added later without touching any other Model's Logic. ``model_type`` is
    declared as the base ``m.BaseModel`` for the class itself, since a
    subclass narrows it to its own concrete Model; the ``cast`` calls below
    only restate that narrowing for the type checker.
    """

    model_type: ClassVar[type[m.BaseModel]]

    def create(self, *, unit=None, **fields) -> ModelT:
        return cast(ModelT, data_access.create(self.model_type, unit=unit, **fields))

    def get(self, id: int, *, unit=None) -> ModelT:
        return cast(ModelT, data_access.get(self.model_type, id, unit=unit))

    def list(
        self, *, unit=None, limit: int | None = None, offset: int = 0, **criteria
    ) -> list[ModelT]:
        records = data_access.list_records(
            self.model_type, unit=unit, limit=limit, offset=offset, **criteria
        )
        return cast(list[ModelT], records)

    def update(self, id: int, *, unit=None, **fields) -> ModelT:
        return cast(ModelT, data_access.update(self.model_type, id, unit=unit, **fields))

    def delete(self, id: int, *, unit=None) -> None:
        data_access.delete(self.model_type, id, unit=unit)

    def set_status(self, id: int, action: Literal["enable", "disable"], *, unit=None) -> ModelT:
        return cast(ModelT, data_access.set_status(self.model_type, id, action, unit=unit))
