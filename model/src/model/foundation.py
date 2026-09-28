"""Foundation layer.

Shared behaviour available to every Entity: conversion of an Entity to JSON and
construction of an Entity from JSON. Foundation declares no Fields, constraints,
or domain meaning of its own.
"""

import json
from typing import Self

from sqlmodel import SQLModel


class Foundation(SQLModel):
    """Base of every Entity; supplies JSON conversion and construction."""

    def to_json(self) -> str:
        """Convert this Entity into a JSON document of its own Fields."""
        return json.dumps(self.model_dump(mode="json"))

    @classmethod
    def from_json(cls, data: str | bytes | bytearray) -> Self:
        """Construct an Entity from a JSON document of its Fields."""
        return cls.model_validate(json.loads(data))
