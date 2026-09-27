"""Shared declaration metadata common to every Domain Entity."""

from typing import Optional

from sqlmodel import Field, SQLModel


class Model_Declaration(SQLModel):
    """Base declaration providing the identity and status Fields every Domain Entity shares."""

    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
