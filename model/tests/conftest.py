"""Shared pytest fixtures for the Model test suite."""

from __future__ import annotations

import datetime


def utc_now() -> datetime.datetime:
    return datetime.datetime(2026, 1, 1, tzinfo=datetime.UTC)
