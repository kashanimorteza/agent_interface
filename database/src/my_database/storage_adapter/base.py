"""Declarative base and naming conventions of the storage schema."""

from sqlalchemy import MetaData, Numeric
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """Base of every mapped table; each subclass declares ``__model_key__`` with its source Model key."""

    metadata = metadata


def decimal_type() -> Numeric:
    """The resolved storage type of every logical decimal field."""
    return Numeric(precision=18, scale=8)
