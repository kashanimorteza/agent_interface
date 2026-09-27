"""User Domain Entity: an independent user of the system."""

from sqlmodel import Field

from my_model.model_declaration import Model_Declaration
from my_model.model_foundation import Model_Foundation


class User(Model_Declaration, Model_Foundation, table=True):
    """An independent user of the system, enabling multi-user operation."""

    __tablename__ = "user"

    name: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False, schema_extra={"sensitivity_marker": "password"})
    api_key: str = Field(nullable=False, schema_extra={"sensitivity_marker": "password"})
