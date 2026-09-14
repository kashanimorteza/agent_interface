"""Application Outcomes Logic produces (consumed by task P3-G11-T1's error mapping)."""

from __future__ import annotations


class ApplicationOutcome(Exception):
    """Base class for every explicit outcome Logic produces."""


class NotFound(ApplicationOutcome):
    def __init__(self, model_name: str, id_: int) -> None:
        super().__init__(f"{model_name} with id={id_} was not found")
        self.model_name = model_name
        self.id = id_


class ValidationFailed(ApplicationOutcome):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class ConflictOutcome(ApplicationOutcome):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail


class Unauthenticated(ApplicationOutcome):
    pass


class Unauthorized(ApplicationOutcome):
    pass
