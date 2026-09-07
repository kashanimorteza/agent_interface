"""The common operation baseline every Model Logic unit adopts.

A unit names its Model and inherits create, get, list, update, and delete.
Input is validated against the shared Model before persistence is reached,
and persistence is reached only through Data Access.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, ClassVar, Generic, TypeVar

from my_model import Model
from pydantic import ValidationError

from ..data_access import DataAccess
from ..outcomes import InvalidData

M = TypeVar("M", bound=Model)

SAFE_ERROR_KEYS = ("type", "loc", "msg")


def sanitize_errors(exc: ValidationError) -> list[dict[str, Any]]:
    """Validation errors without the offending input, which may be a credential."""
    return [{k: v for k, v in error.items() if k in SAFE_ERROR_KEYS} for error in exc.errors()]


class ModelLogic(Generic[M]):
    model: ClassVar[type[Model]]

    def __init__(self, data_access: DataAccess) -> None:
        self.data_access = data_access

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        model = getattr(cls, "model", None)
        if not (isinstance(model, type) and issubclass(model, Model) and model is not Model):
            raise TypeError(f"{cls.__name__} must name the shared Model it belongs to")

    # -- standard operations -------------------------------------------------

    def create(self, data: Mapping[str, Any]) -> M:
        value = self.validate(data)
        return self.data_access.create(value)

    def get(self, key: Any) -> M:
        return self.data_access.get(self.model, key)

    def list(self, criteria: Mapping[str, Any] | None = None) -> list[M]:
        return self.data_access.list(self.model, criteria)

    def update(self, key: Any, changes: Mapping[str, Any]) -> M:
        current = self.get(key)
        self.validate({**current.model_dump(), **changes})
        return self.data_access.update(self.model, key, changes)

    def delete(self, key: Any) -> None:
        self.data_access.delete(self.model, key)

    # -- domain validation ---------------------------------------------------

    def validate(self, data: Mapping[str, Any]) -> M:
        """A shared-Model instance, or the invalid-data outcome."""
        try:
            return self.model.model_validate(dict(data))
        except ValidationError as exc:
            raise InvalidData(self.model.__name__, sanitize_errors(exc)) from None
