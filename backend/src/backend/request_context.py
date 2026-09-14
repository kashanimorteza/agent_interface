"""The Request Context every request carries: a non-secret request identifier and, once
authenticated, the requester's identity. Never carries a Credential value."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RequestContext:
    request_id: str
    user_id: int | None = None

    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None
