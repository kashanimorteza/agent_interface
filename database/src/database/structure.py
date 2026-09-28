"""Storage structure derived from the Entities that Model publishes."""

import model.interface  # noqa: F401  Importing the Entities registers one Table for each of them.
from sqlalchemy import MetaData
from sqlmodel import SQLModel

metadata: MetaData = SQLModel.metadata
