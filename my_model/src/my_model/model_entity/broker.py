"""The Broker Entity."""

from typing import ClassVar

from sqlalchemy import UniqueConstraint
from sqlmodel import Field

from my_model.model_declaration import (
    FieldDeclaration,
    Model_Declaration,
    ReferenceDeclaration,
)
from my_model.model_foundation import Model_Foundation


class Broker(Model_Foundation, table=True):
    """A broker supported by the system, owned by a user and not coupled to one Trading Platform."""

    declaration: ClassVar[Model_Declaration] = Model_Declaration(
        entity="Broker",
        purpose="A broker supported by the system, owned by a user and not coupled to one Trading Platform.",
        fields=(
            FieldDeclaration(
                name="id",
                type="integer",
                nullable=False,
                value_generation="auto_increment",
            ),
            FieldDeclaration(
                name="name",
                type="string",
                nullable=False,
                purpose="The broker's display name.",
            ),
            FieldDeclaration(
                name="user_id",
                type="integer",
                nullable=False,
                purpose="Identifies the user who owns the broker configuration.",
            ),
            FieldDeclaration(
                name="is_active",
                type="boolean",
                nullable=False,
                purpose="Indicates whether the broker is active.",
                has_default=True,
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type="string",
                nullable=True,
                purpose="Describes the broker.",
            ),
        ),
        references=(ReferenceDeclaration(field="user_id", entity="User"),),
        unique_constraints=(("user_id", "name"),),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id")
    is_active: bool = True
    description: str | None = None
