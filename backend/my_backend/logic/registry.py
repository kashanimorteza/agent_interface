"""The registry through which a Model resolves to its Logic unit.

The registry imports and connects the units; it defines none of them.
"""

from __future__ import annotations

from collections.abc import Iterator

from my_model import Model

from ..data_access import DataAccess
from ..outcomes import NoLogicUnit
from .base import ModelLogic


class LogicRegistry:
    def __init__(self, data_access: DataAccess) -> None:
        self._data_access = data_access
        self._units: dict[type[Model], ModelLogic] = {}

    def register(self, unit_class: type[ModelLogic]) -> ModelLogic:
        model = unit_class.model
        if model in self._units:
            raise ValueError(f"{model.__name__} already has a Logic unit")
        unit = unit_class(self._data_access)
        self._units[model] = unit
        return unit

    def for_model(self, model: type[Model]) -> ModelLogic:
        try:
            return self._units[model]
        except KeyError:
            raise NoLogicUnit(getattr(model, "__name__", repr(model))) from None

    def __iter__(self) -> Iterator[ModelLogic]:
        return iter(self._units.values())

    def __len__(self) -> int:
        return len(self._units)

    def __contains__(self, model: object) -> bool:
        return model in self._units


def build_registry(data_access: DataAccess) -> LogicRegistry:
    """A registry holding every defined unit."""
    from .units import UNITS

    registry = LogicRegistry(data_access)
    for unit_class in UNITS:
        registry.register(unit_class)
    return registry
