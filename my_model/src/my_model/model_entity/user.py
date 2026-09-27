"""User: an independent user of the system, enabling multi-user operation."""

from sqlmodel import Field

from my_model.model_declaration import Model_Declaration


class User(Model_Declaration, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False, schema_extra={"sensitivity": "password"})
    api_key: str = Field(nullable=False, schema_extra={"sensitivity": "sensitive"})
    is_active: bool = Field(default=True, nullable=False)
    description: str | None = Field(default=None)
