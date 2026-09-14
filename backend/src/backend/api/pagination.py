"""Bounded, cursor-based, allowlisted list queries (task P3-G10-T3).

List requests accept only `cursor` and `limit`. Search requests may additionally provide
declared Model fields; the generic router validates those fields before querying.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Annotated, Any, TypeVar

from fastapi import Query, Request

from ..logic.outcomes import ValidationFailed

DEFAULT_LIMIT = 50
MAXIMUM_LIMIT = 100
ALLOWED_LIST_QUERY_PARAMS = frozenset({"cursor", "limit"})

T = TypeVar("T")


@dataclass(slots=True)
class PaginationParams:
    cursor: int | None
    limit: int


def get_pagination(
    request: Request,
    cursor: Annotated[int | None, Query(ge=1)] = None,
    limit: Annotated[int, Query(ge=1, le=MAXIMUM_LIMIT)] = DEFAULT_LIMIT,
) -> PaginationParams:
    unexpected = set(request.query_params) - ALLOWED_LIST_QUERY_PARAMS
    if request.url.path.endswith("/search"):
        unexpected = set()
    if unexpected:
        raise ValidationFailed(f"Unsupported query parameter(s): {sorted(unexpected)}")
    return PaginationParams(cursor=cursor, limit=min(limit, MAXIMUM_LIMIT))


def apply_pagination(items: Sequence[Any], params: PaginationParams) -> list[Any]:
    ordered = sorted(items, key=lambda item: item.id)
    if params.cursor is not None:
        ordered = [item for item in ordered if item.id > params.cursor]
    return ordered[: params.limit]
