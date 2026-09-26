"""Entity classes and table metadata that Database persists, taken from Model's public entry point."""

import my_model.interface as model
from sqlalchemy import MetaData
from sqlmodel import SQLModel

ENTITIES: tuple[type[SQLModel], ...] = tuple(
    item
    for name in model.__all__
    if isinstance(item := getattr(model, name), type)
    and issubclass(item, SQLModel)
    and hasattr(item, "__table__")
)


def metadata() -> MetaData:
    """Return the table metadata of every imported Entity.

    Returns:
        (MetaData): The authoritative metadata for table creation and migration comparison.
    """
    return SQLModel.metadata
