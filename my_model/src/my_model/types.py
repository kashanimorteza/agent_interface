"""Reusable domain types shared by more than one Model in this package."""

from decimal import Decimal
from typing import Annotated

from pydantic import Field

Percentage = Annotated[Decimal, Field(ge=0, le=100)]
"""A percentage value between 0 and 100 inclusive, shared by every rule expressing one."""
