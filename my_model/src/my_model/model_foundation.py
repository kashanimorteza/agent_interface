"""Model_Foundation: shared to_json()/from_json() conversion behaviour used by every Domain Entity."""

from typing import Any


class Model_Foundation:
    def to_json(self) -> dict[str, Any]:
        return self.model_dump(mode="json")  # type: ignore[attr-defined]

    @classmethod
    def from_json(cls, data: dict[str, Any]):
        return cls.model_validate(data)  # type: ignore[attr-defined]
