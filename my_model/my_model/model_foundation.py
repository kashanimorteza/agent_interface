"""Shared JSON conversion behaviour common to every Domain Entity."""

from typing import Any, Dict, Type, TypeVar

from sqlmodel import SQLModel

T = TypeVar("T", bound="Model_Foundation")


class Model_Foundation(SQLModel):
    """Base foundation providing to_json() and from_json() without domain meaning of its own."""

    def to_json(self) -> Dict[str, Any]:
        return self.model_dump(mode="json")

    @classmethod
    def from_json(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls.model_validate(data)
