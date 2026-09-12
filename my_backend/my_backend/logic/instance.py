"""Instance Model Logic.

Extends the generic base with the Target-declared rule that the selected
Trading Platform determines which of Instance's connection fields are
required. Neither Model (a single-record boundary) nor Database (a
persisted-state boundary) can enforce this rule: it depends on operation
context together with a referenced entity's own data, so it belongs here.

The Target names two Trading Platforms without enumerating which connection
field each one requires; this mapping is therefore a consequential
implementation choice, recorded here rather than left undecided.
"""

from __future__ import annotations

from typing import Any

from my_backend import _database_interface as db
from my_backend import _model_interface as model
from my_backend._errors import MissingPlatformRequiredFieldError
from my_backend.logic._base import ModelLogic

PLATFORM_REQUIRED_FIELDS: dict[str, list[str]] = {
    "metatrader_5": ["ip", "username", "password"],
    "binance": ["api_key"],
}


class InstanceLogic(ModelLogic[model.Instance]):
    def __init__(self) -> None:
        super().__init__(model.Instance)

    def _validate_platform_requirements(self, data: dict[str, Any]) -> None:
        platform = db.get(model.TradingPlatform, data["trading_platform_id"])
        required = PLATFORM_REQUIRED_FIELDS.get(platform.code, [])
        missing = [field for field in required if not data.get(field)]
        if missing:
            raise MissingPlatformRequiredFieldError(
                f"Trading Platform {platform.code!r} requires {missing!r}, which this Instance omits."
            )

    def create(self, data: dict[str, Any]) -> model.Instance:
        self._validate_platform_requirements(data)
        return super().create(data)

    def update(self, id: int, patch: dict[str, Any]) -> model.Instance:
        current = self.get(id)
        merged = {**current.model_dump(), **patch}
        self._validate_platform_requirements(merged)
        return super().update(id, patch)


logic = InstanceLogic()
