"""Shared SQLAlchemy declarative base for every persistence mapping."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
