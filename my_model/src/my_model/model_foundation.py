"""Shared Model behaviour: conversion of an Entity to and from JSON."""

import json
from typing import Self

from sqlmodel import SQLModel


class ModelFoundation(SQLModel):
    """Base for every Entity. Supplies conversion behaviour and defines no Fields."""

    def to_json(self) -> str:
        """Convert the instance to a JSON string.

        Returns:
            (str): JSON representation of the instance.
        """
        return self.model_dump_json()

    @classmethod
    def from_json(cls, data: str | bytes) -> Self:
        """Create an instance from a JSON string.

        Args:
            data (str | bytes): JSON representation of the instance.

        Returns:
            (Self): Validated instance of the calling Entity.
        """
        return cls.model_validate(json.loads(data))
