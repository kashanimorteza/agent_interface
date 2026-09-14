"""The shared declarative base and column types every storage mapping in this phase builds on."""

from __future__ import annotations

import datetime
from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import TypeDecorator


class Base(DeclarativeBase):
    """The shared SQLAlchemy declarative base for every storage mapping."""


class UTCDateTime(TypeDecorator[datetime.datetime]):
    """Stores a timezone-aware datetime as UTC; rejects a naive datetime on the way in."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(
        self, value: datetime.datetime | None, dialect: Any
    ) -> datetime.datetime | None:
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("datetime value must be timezone-aware")
        return value.astimezone(datetime.UTC).replace(tzinfo=None)

    def process_result_value(
        self, value: datetime.datetime | None, dialect: Any
    ) -> datetime.datetime | None:
        if value is None:
            return None
        return value.replace(tzinfo=datetime.UTC)
