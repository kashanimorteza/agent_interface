"""Common behaviour shared by every Entity."""

from typing import Any

from model.core.foundation import Foundation
from model.core.validation import check_assignment, resolve_values, validate_defaults


class Entity(Foundation):
    """Base of every Entity; enforces the Field contracts of its Declaration."""

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """Reject an Entity whose Declaration disagrees with its own class."""
        super().__pydantic_init_subclass__(**kwargs)
        validate_defaults(cls.declaration)
        declared = [f.name for f in cls.declaration.fields]
        if list(cls.model_fields) != declared:
            raise ValueError(
                f"{cls.declaration.name}: class Fields do not match the Declaration"
            )

    def __init__(self, **data: Any) -> None:
        super().__init__(**resolve_values(self.declaration, data))

    def __setattr__(self, name: str, value: Any) -> None:
        check_assignment(self.declaration, self.__dict__, name, value)
        super().__setattr__(name, value)
